# -----------------------------------------------------------
# Intelligent Tutoring System 
# Author: Kunal Badhan | Chandigarh University
# -----------------------------------------------------------

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json, os, random, time
import matplotlib.pyplot as plt
import networkx as nx

DATA_FILE = "data.json"

# ---------- Splash Screen ----------
def show_splash(root):
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("500x320+450+250")

    canvas = tk.Canvas(splash, width=500, height=320, highlightthickness=0)
    canvas.pack()

    for i in range(320):
        color = "#%02x%02x%02x" % (173, 216 - i//5, 230)
        canvas.create_line(0, i, 500, i, fill=color)

    canvas.create_text(250, 130, text="Intelligent Tutoring System",
                       font=("Helvetica", 18, "bold"), fill="navy")
    canvas.create_text(250, 170, text="AI Edition", font=("Helvetica", 14), fill="darkblue")

    progress = ttk.Progressbar(splash, orient="horizontal", length=400, mode="determinate")
    progress.place(x=50, y=250)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TProgressbar", troughcolor="#DFF3FF", background="navy", thickness=15)

    root.withdraw()

    def animate(i=0):
        if i <= 100:
            progress["value"] = i
            splash.update_idletasks()
            splash.after(20, lambda: animate(i + 2))
        else:
            splash.destroy()
            root.deiconify()

    animate()

# ---------- Data Management ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        data = {
            "AI Tools": {"score": 0, "attempts": 0},
            "ADBMS": {"score": 0, "attempts": 0},
            "Python Programming": {"score": 0, "attempts": 0}
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
        return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Quiz Data ----------
QUIZ_DATA = {
    "AI Tools": [
        {"type": "mcq", "question": "Which of these is an AI framework by Google?",
         "options": ["TensorFlow", "React", "Bootstrap", "Docker"], "answer": "TensorFlow"},
        {"type": "text", "question": "Name one popular AI programming language.", "answer": "python"},
        {"type": "mcq", "question": "What does NLP stand for?",
         "options": ["Natural Language Processing", "Neural Logic Program", "Network Learning Process", "None"],
         "answer": "Natural Language Processing"}
    ],
    "ADBMS": [
        {"type": "mcq", "question": "Which of these is an example of an ADBMS?",
         "options": ["Oracle 12c", "MS Word", "Google Chrome", "Photoshop"], "answer": "Oracle 12c"},
        {"type": "text", "question": "What does ADBMS stand for?", "answer": "advanced database management system"},
        {"type": "mcq", "question": "Which command retrieves data from a database?",
         "options": ["SELECT", "DELETE", "INSERT", "UPDATE"], "answer": "SELECT"}
    ],
    "Python Programming": [
        {"type": "mcq", "question": "Which keyword is used to define a function in Python?",
         "options": ["def", "function", "define", "fun"], "answer": "def"},
        {"type": "text", "question": "What symbol is used for comments in Python?", "answer": "#"},
        {"type": "mcq", "question": "Which library is used for numerical computation?",
         "options": ["NumPy", "Pandas", "Tkinter", "Flask"], "answer": "NumPy"}
    ]
}

# ---------- Main App ----------
class IntelligentTutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Tutoring System — AI Edition")
        self.root.geometry("1000x650")
        self.root.configure(bg="#E6F3FF")
        self.data = load_data()
        self.file_paths = []  # store full paths of uploaded study materials

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"),
                        padding=6, background="#5A9BD5", foreground="white")
        style.map("TButton", background=[("active", "#4C8DC5")])
        style.configure("Hover.TButton", background="#1E6091")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.study_tab = ttk.Frame(self.notebook)
        self.quiz_tab = ttk.Frame(self.notebook)
        self.performance_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.study_tab, text="📘 Study")
        self.notebook.add(self.quiz_tab, text="🧠 Quiz")
        self.notebook.add(self.performance_tab, text="📊 Performance")

        self.setup_study_tab()
        self.setup_quiz_tab()
        self.setup_performance_tab()

    # ---------- Helper ----------
    def make_gradient(self, frame):
        canvas = tk.Canvas(frame, width=1000, height=650, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        for i in range(0, 650, 2):
            color = "#%02x%02x%02x" % (210, 240 - i//6, 255)
            canvas.create_line(0, i, 1000, i, fill=color)

    def add_hover_effects(self, widget):
        def on_enter(e): e.widget.configure(style="Hover.TButton")
        def on_leave(e): e.widget.configure(style="TButton")
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    # ---------- Study Tab ----------
    def setup_study_tab(self):
        self.make_gradient(self.study_tab)
        ttk.Label(self.study_tab, text="📚 Upload & Manage Study Material",
                  font=("Segoe UI", 14, "bold"), background="#DFF3FF").pack(pady=15)

        card = tk.Frame(self.study_tab, bg="white", bd=3, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center", width=700, height=350)

        ttk.Label(card, text="Select Subject:", font=("Segoe UI", 11, "bold"), background="white").pack(pady=10)
        self.subject_var = tk.StringVar(value="AI Tools")
        ttk.Combobox(card, textvariable=self.subject_var, values=list(QUIZ_DATA.keys()),
                     state="readonly").pack(pady=5)

        list_frame = tk.Frame(card, bg="white")
        list_frame.pack(pady=10)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        self.file_list = tk.Listbox(list_frame, height=7, width=70, yscrollcommand=scrollbar.set,
                                    font=("Segoe UI", 9), bg="#F2F8FF", relief="flat")
        self.file_list.pack(side="left", fill="both", padx=10)
        scrollbar.config(command=self.file_list.yview)

        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(pady=15)
        attach_btn = ttk.Button(btn_frame, text="📎 Attach Study File", command=self.add_file)
        open_btn = ttk.Button(btn_frame, text="📂 Open Selected File", command=self.open_file)
        attach_btn.grid(row=0, column=0, padx=10)
        open_btn.grid(row=0, column=1, padx=10)
        self.add_hover_effects(attach_btn)
        self.add_hover_effects(open_btn)

    def add_file(self):
        fpath = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.docx *.pptx")])
        if fpath:
            filename = os.path.basename(fpath)
            self.file_list.insert(tk.END, filename)
            self.file_paths.append(fpath)
            messagebox.showinfo("✅ File Added", f"File '{filename}' attached successfully for study!")

    def open_file(self):
        sel = self.file_list.curselection()
        if not sel:
            messagebox.showwarning("⚠️ No Selection", "Please select a file to open.")
            return
        index = sel[0]
        if index < len(self.file_paths):
            path = self.file_paths[index]
            if os.path.exists(path):
                os.startfile(path)
            else:
                messagebox.showerror("❌ File Not Found", f"The file path no longer exists:\n{path}")
        else:
            messagebox.showerror("⚠️ Missing File Info", "File path not stored. Try re-adding the file.")

    # ---------- Quiz Tab ----------
    def setup_quiz_tab(self):
        self.make_gradient(self.quiz_tab)
        ttk.Label(self.quiz_tab, text="🧠 Choose a Subject to Begin Quiz:",
                  font=("Segoe UI", 13, "bold"), background="#DFF3FF").pack(pady=15)
        self.quiz_subject = tk.StringVar(value="AI Tools")
        ttk.Combobox(self.quiz_tab, textvariable=self.quiz_subject, values=list(QUIZ_DATA.keys()),
                     state="readonly").pack(pady=5)
        start_btn = ttk.Button(self.quiz_tab, text="Start Quiz", command=self.start_quiz)
        start_btn.pack(pady=15)
        self.add_hover_effects(start_btn)
        self.quiz_frame = ttk.Frame(self.quiz_tab)
        self.quiz_frame.pack(pady=20)

    def start_quiz(self):
        for w in self.quiz_frame.winfo_children():
            w.destroy()
        subject = self.quiz_subject.get()
        qlist = random.sample(QUIZ_DATA[subject], len(QUIZ_DATA[subject]))
        self.current, self.correct, self.questions = 0, 0, qlist
        self.show_question()

    def show_question(self):
        for w in self.quiz_frame.winfo_children():
            w.destroy()
        if self.current >= len(self.questions):
            self.end_quiz()
            return
        q = self.questions[self.current]
        ttk.Label(self.quiz_frame, text=f"Q{self.current + 1}. {q['question']}",
                  font=("Segoe UI", 11)).pack(pady=10)
        self.answer_var = tk.StringVar()
        if q["type"] == "mcq":
            for opt in q["options"]:
                ttk.Radiobutton(self.quiz_frame, text=opt, variable=self.answer_var, value=opt).pack(anchor="w", padx=40)
        else:
            ttk.Entry(self.quiz_frame, textvariable=self.answer_var, width=40).pack(pady=5)
        submit_btn = ttk.Button(self.quiz_frame, text="Submit", command=self.check_answer)
        submit_btn.pack(pady=10)
        self.add_hover_effects(submit_btn)

    def check_answer(self):
        ans = self.answer_var.get().strip().lower()
        q = self.questions[self.current]
        if ans == q["answer"].lower():
            self.correct += 1
        self.current += 1
        self.show_question()

    def end_quiz(self):
        total = len(self.questions)
        score = int((self.correct / total) * 100)
        subject = self.quiz_subject.get()
        self.data[subject]["attempts"] += 1
        self.data[subject]["score"] = int((self.data[subject]["score"] + score) / 2)
        save_data(self.data)
        msg = "🌟 Excellent! You're ready for harder topics." if score > 80 else \
              "✅ Good effort! Revise and retry for better results." if score > 50 else \
              "⚠️ Needs improvement. Review study material and retry."
        messagebox.showinfo("Quiz Completed", f"Your Score: {score}%\n\n{msg}")

    # ---------- Performance Tab ----------
    def setup_performance_tab(self):
        self.make_gradient(self.performance_tab)
        ttk.Label(self.performance_tab, text="📊 Performance Overview",
                  font=("Segoe UI", 13, "bold"), background="#DFF3FF").pack(pady=10)
        for text, cmd in [
            ("Show Bar Chart", self.show_bar_chart),
            ("Show Pie Chart", self.show_pie_chart),
            ("Show Knowledge Graph", self.show_knowledge_graph),
            ("Show Recommendations", self.show_recommendations)
        ]:
            btn = ttk.Button(self.performance_tab, text=text, command=cmd)
            btn.pack(pady=5)
            self.add_hover_effects(btn)

    def show_bar_chart(self):
        subjects = list(self.data.keys())
        scores = [self.data[s]["score"] for s in subjects]
        plt.figure(figsize=(6, 4))
        plt.bar(subjects, scores, color=["#5A9BD5", "#66CC99", "#FFCC66"])
        plt.title("Performance by Subject")
        plt.ylabel("Average Score (%)")
        plt.xlabel("Subjects")
        plt.ylim(0, 100)
        plt.show()

    def show_pie_chart(self):
        subjects = list(self.data.keys())
        scores = [max(self.data[s]["score"], 1) for s in subjects]
        plt.figure(figsize=(5, 5))
        plt.pie(scores, labels=subjects, autopct="%1.1f%%",
                colors=["#5A9BD5", "#66CC99", "#FFCC66"], startangle=90)
        plt.title("Overall Knowledge Distribution")
        plt.show()

    def show_knowledge_graph(self):
        G = nx.Graph()
        for s, d in self.data.items():
            G.add_node(s, score=d["score"])
        G.add_edges_from([
            ("AI Tools", "ADBMS"),
            ("AI Tools", "Python Programming"),
            ("ADBMS", "Python Programming")
        ])
        colors = ["green" if d["score"] >= 80 else "orange" if d["score"] >= 50 else "red"
                  for s, d in self.data.items()]
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color=colors,
                node_size=2000, font_color="white", font_size=10, font_weight="bold")
        plt.title("Knowledge Graph — Student Mastery Levels")
        plt.show()

    def show_recommendations(self):
        msg = "📖 Personalized Study Recommendations:\n\n"
        for s, d in self.data.items():
            score = d["score"]
            if score >= 80:
                rec = "Advance to complex topics or practical applications."
            elif score >= 50:
                rec = "Revise core concepts and practice medium-level exercises."
            else:
                rec = "Revisit basics and go through easier study material."
            msg += f"{s}: {rec}\n"
        messagebox.showinfo("Recommendations", msg)

# ---------- Run ----------
if __name__ == "__main__":
    root = tk.Tk()
    show_splash(root)
    app = IntelligentTutorApp(root)
    root.mainloop()
