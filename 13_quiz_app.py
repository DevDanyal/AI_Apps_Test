import tkinter as tk
from tkinter import messagebox
import random

class QuizGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Application")
        
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "answer": "Paris"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Mars", "Venus", "Jupiter", "Saturn"],
                "answer": "Mars"
            },
            {
                "question": "What is the largest mammal in the world?",
                "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
                "answer": "Blue Whale"
            },
            {
                "question": "Who wrote the play 'Romeo and Juliet'?",
                "options": ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"],
                "answer": "William Shakespeare"
            },
            {
                "question": "What is the chemical symbol for gold?",
                "options": ["Au", "Ag", "Fe", "Cu"],
                "answer": "Au"
            }
        ]
        
        self.score = 0
        self.current_question = -1
        
        self.question_label = tk.Label(self.master, text="", font=("normal", 16), wraplength=400)
        self.question_label.pack(pady=20)
        
        self.var = tk.StringVar()
        
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.master, text="", variable=self.var, value="", font=("normal", 12))
            self.radio_buttons.append(rb)
            rb.pack(anchor="w", padx=50)
            
        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=20)
        
        self.next_button = tk.Button(self.master, text="Next", command=self.next_question, state="disabled")
        self.next_button.pack(pady=10)
        
        self.start_quiz()

    def start_quiz(self):
        random.shuffle(self.questions)
        self.score = 0
        self.current_question = -1
        self.next_question()

    def next_question(self):
        self.current_question += 1
        
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.question_label.config(text=q["question"])
            
            options = q["options"]
            random.shuffle(options)
            
            self.var.set("")
            for i in range(4):
                self.radio_buttons[i].config(text=options[i], value=options[i])
            
            self.submit_button.config(state="normal")
            self.next_button.config(state="disabled")
        else:
            self.show_score()

    def check_answer(self):
        selected_option = self.var.get()
        correct_answer = self.questions[self.current_question]["answer"]
        
        if selected_option == correct_answer:
            self.score += 1
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showerror("Result", f"Wrong! The correct answer is {correct_answer}.")
            
        self.submit_button.config(state="disabled")
        self.next_button.config(state="normal")

    def show_score(self):
        messagebox.showinfo("Quiz Over", f"Your final score is {self.score}/{len(self.questions)}.")
        if messagebox.askyesno("Play Again?", "Do you want to play another round?"):
            self.start_quiz()
        else:
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGUI(root)
    root.mainloop()
