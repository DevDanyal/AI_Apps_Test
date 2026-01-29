import tkinter as tk
from tkinter import messagebox
import time
import random

class TypingSpeedTest:
    def __init__(self, master):
        self.master = master
        master.title("Typing Speed Test")
        master.geometry("800x500")
        master.resizable(False, False)

        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Python is a high-level, interpreted programming language.",
            "Practice makes perfect when it comes to typing.",
            "The early bird catches the worm, but the second mouse gets the cheese.",
            "A journey of a thousand miles begins with a single step."
        ]
        self.current_text = ""
        self.start_time = None
        self.end_time = None
        self.timer_running = False

        self.create_widgets()
        self.reset_test()

    def create_widgets(self):
        # Display frame for text to type
        text_frame = tk.Frame(self.master, padx=10, pady=10, bd=2, relief="groove")
        text_frame.pack(pady=10, fill=tk.X)

        self.display_text = tk.Label(text_frame, text="", wraplength=750, justify=tk.LEFT, font=("Arial", 14))
        self.display_text.pack()

        # Input frame for user typing
        input_frame = tk.Frame(self.master, padx=10, pady=5)
        input_frame.pack(pady=5, fill=tk.X)

        self.user_input = tk.Text(input_frame, height=5, width=70, font=("Arial", 14))
        self.user_input.pack()
        self.user_input.bind("<KeyRelease>", self.start_timer_and_check)
        self.user_input.config(state=tk.DISABLED) # Disable until test starts

        # Controls and results frame
        controls_results_frame = tk.Frame(self.master, padx=10, pady=10)
        controls_results_frame.pack(fill=tk.X)

        self.timer_label = tk.Label(controls_results_frame, text="Time: 0s", font=("Arial", 12))
        self.timer_label.grid(row=0, column=0, padx=20)

        self.wpm_label = tk.Label(controls_results_frame, text="WPM: 0", font=("Arial", 12))
        self.wpm_label.grid(row=0, column=1, padx=20)

        self.accuracy_label = tk.Label(controls_results_frame, text="Accuracy: 0%", font=("Arial", 12))
        self.accuracy_label.grid(row=0, column=2, padx=20)

        self.start_button = tk.Button(controls_results_frame, text="Start Test", command=self.start_test, font=("Arial", 12, "bold"))
        self.start_button.grid(row=0, column=3, padx=20)

        self.reset_button = tk.Button(controls_results_frame, text="Reset", command=self.reset_test, font=("Arial", 12))
        self.reset_button.grid(row=0, column=4, padx=20)

    def reset_test(self):
        self.current_text = random.choice(self.sample_texts)
        self.display_text.config(text=self.current_text)
        self.user_input.config(state=tk.NORMAL)
        self.user_input.delete(1.0, tk.END)
        self.user_input.config(state=tk.DISABLED)
        self.start_time = None
        self.end_time = None
        self.timer_running = False
        self.timer_label.config(text="Time: 0s")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")
        self.start_button.config(state=tk.NORMAL)

    def start_test(self):
        self.user_input.config(state=tk.NORMAL)
        self.user_input.focus_set()
        self.start_button.config(state=tk.DISABLED)
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def start_timer_and_check(self, event):
        if not self.timer_running:
            self.start_test()
        
        # Check if the user has typed enough characters to potentially end the test
        typed_content = self.user_input.get(1.0, tk.END).strip()
        if typed_content == self.current_text:
            self.end_test()
        
    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.master.after(1000, self.update_timer) # Update every second

    def end_test(self):
        self.timer_running = False
        self.end_time = time.time()
        self.user_input.config(state=tk.DISABLED)
        self.calculate_results()

    def calculate_results(self):
        typed_text = self.user_input.get(1.0, tk.END).strip()
        original_text = self.current_text

        time_taken = self.end_time - self.start_time
        if time_taken == 0:
            time_taken = 1 # Avoid division by zero

        # Calculate WPM
        words_typed = len(typed_text.split())
        wpm = int((words_typed / time_taken) * 60)
        self.wpm_label.config(text=f"WPM: {wpm}")

        # Calculate Accuracy
        correct_chars = 0
        min_len = min(len(typed_text), len(original_text))
        for i in range(min_len):
            if typed_text[i] == original_text[i]:
                correct_chars += 1
        
        accuracy = (correct_chars / len(original_text)) * 100 if len(original_text) > 0 else 0
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
