import tkinter as tk
from tkinter import messagebox
import random

class MathPracticeApp:
    def __init__(self, master):
        self.master = master
        master.title("Math Practice App")
        master.geometry("500x400")
        master.resizable(False, False)

        self.score = 0
        self.total_questions = 0
        self.current_answer = 0

        self.create_widgets()
        self.generate_question()

    def create_widgets(self):
        # Question display
        self.question_label = tk.Label(self.master, text="Question", font=("Arial", 24))
        self.question_label.pack(pady=20)

        # Answer input
        self.answer_entry = tk.Entry(self.master, width=20, font=("Arial", 18))
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind("<Return>", self.check_answer_event)

        # Buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        self.submit_button = tk.Button(button_frame, text="Submit", command=self.check_answer, font=("Arial", 14))
        self.submit_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(button_frame, text="Next Question", command=self.generate_question, font=("Arial", 14))
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_game, font=("Arial", 14))
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Score and feedback
        self.score_label = tk.Label(self.master, text="Score: 0/0", font=("Arial", 16))
        self.score_label.pack(pady=10)

        self.feedback_label = tk.Label(self.master, text="", font=("Arial", 16), fg="blue")
        self.feedback_label.pack(pady=5)

    def generate_question(self):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operators = ['+', '-', '*']
        operator = random.choice(operators)

        question_text = f"{num1} {operator} {num2} ="
        self.question_label.config(text=question_text)

        if operator == '+':
            self.current_answer = num1 + num2
        elif operator == '-':
            self.current_answer = num1 - num2
        elif operator == '*':
            self.current_answer = num1 * num2
        # Division can be added with more careful handling of remainders and zero division

        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        self.answer_entry.focus_set()

    def check_answer_event(self, event):
        self.check_answer()

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            self.total_questions += 1
            
            if user_answer == self.current_answer:
                self.score += 1
                self.feedback_label.config(text="Correct!", fg="green")
            else:
                self.feedback_label.config(text=f"Incorrect! The answer was {self.current_answer}", fg="red")
            
            self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
            # Automatically move to next question after a short delay
            self.master.after(1000, self.generate_question)

        except ValueError:
            self.feedback_label.config(text="Please enter a valid number!", fg="orange")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def reset_game(self):
        self.score = 0
        self.total_questions = 0
        self.score_label.config(text="Score: 0/0")
        self.feedback_label.config(text="")
        self.generate_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathPracticeApp(root)
    root.mainloop()
