import tkinter as tk
from tkinter import messagebox
import json

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🧠 Quiz App")
        self.master.geometry("900x500+300+200")
        self.master.config(bg="#f0f4f8")
        root.resizable(False, False)

        self.load_questions()
        self.q_index = 0
        self.score = 0
        self.answered = False

        self.question_label = tk.Label(master, text="", font=("Arial", 16, "bold"), wraplength=550, bg="#f0f4f8", fg="#333")
        self.question_label.pack(pady=30)

        self.option_var = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(master, text="", variable=self.option_var, value="", font=("Arial", 14),
                                 bg="#f0f4f8", anchor="w", wraplength=500, command=self.check_answer, indicatoron=0,
                                 width=30, padx=10, pady=8, relief="ridge", bd=2)
            btn.pack(pady=5)
            self.radio_buttons.append(btn)

        self.feedback_label = tk.Label(master, text="", font=("Arial", 14, "italic"), bg="#f0f4f8", fg="#555")
        self.feedback_label.pack(pady=10)

        self.next_btn = tk.Button(master, text="Next ➡️", command=self.next_question, font=("Arial", 14),
                                  bg="#007acc", fg="white", padx=15, pady=5, state="disabled")
        self.next_btn.pack(pady=20)

    def load_questions(self):
        with open("questions.json", "r") as f:
            self.questions = json.load(f)

    def show_question(self):
        self.answered = False
        self.feedback_label.config(text="")
        self.option_var.set("")

        q = self.questions[self.q_index]
        self.question_label.config(text=f"Q{self.q_index + 1}: {q['question']}")
        for i in range(4):
            self.radio_buttons[i].config(text=q['options'][i], value=q['options'][i], bg="#f0f4f8", state="normal")
        self.next_btn.config(state="disabled")

    def check_answer(self):
        if self.answered:
            return

        self.answered = True
        selected = self.option_var.get()
        correct = self.questions[self.q_index]["answer"]

        for btn in self.radio_buttons:
            btn.config(state="disabled")

        if selected == correct:
            self.feedback_label.config(text="✅ Correct!", fg="green")
            self.score += 1
        else:
            self.feedback_label.config(text=f"❌ Incorrect! Correct answer is : {correct}", fg="red")

        self.next_btn.config(state="normal")

    def next_question(self):
        self.q_index += 1
        if self.q_index < len(self.questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text=f"🎯 Your Final Score is : {self.score} / {len(self.questions)}", font=("Arial", 18),
                 bg="#f0f4f8", fg="#333").pack(pady=30)

        tk.Button(self.master, text="🔁 Play Again", command=self.restart_quiz, font=("Arial", 14),
                  bg="#4caf50", fg="white", padx=15, pady=8).pack(pady=10)

        tk.Button(self.master, text="❌ Quit", command=self.master.quit, font=("Arial", 14),
                  bg="#f44336", fg="white", padx=15, pady=8).pack(pady=10)

    def restart_quiz(self):
        self.q_index = 0
        self.score = 0
        for widget in self.master.winfo_children():
            widget.destroy()
        self.__init__(self.master)
        self.show_question()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    app.show_question()
    root.mainloop()
