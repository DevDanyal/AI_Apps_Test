
import tkinter as tk
from tkinter import messagebox

class VotingSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voting System")

        self.options = {
            "Option A": 0,
            "Option B": 0,
            "Option C": 0
        }

        self.create_widgets()
        self.update_results_display()

    def create_widgets(self):
        # Title
        tk.Label(self.root, text="Cast Your Vote!", font=("Arial", 16, "bold")).pack(pady=10)

        # Voting Buttons
        self.vote_buttons_frame = tk.Frame(self.root)
        self.vote_buttons_frame.pack(pady=10)

        for option_name in self.options.keys():
            button = tk.Button(self.vote_buttons_frame, text=f"Vote for {option_name}",
                               command=lambda op=option_name: self.cast_vote(op),
                               font=("Arial", 12), width=20, height=2)
            button.pack(pady=5)

        # Results Display
        tk.Label(self.root, text="Current Results:", font=("Arial", 14, "underline")).pack(pady=10)

        self.results_labels = {}
        for option_name in self.options.keys():
            label = tk.Label(self.root, text="", font=("Arial", 12))
            label.pack()
            self.results_labels[option_name] = label

        # Reset Button
        self.reset_button = tk.Button(self.root, text="Reset Votes", command=self.reset_votes,
                                       font=("Arial", 10), bg="red", fg="white")
        self.reset_button.pack(pady=20)

    def cast_vote(self, option):
        self.options[option] += 1
        self.update_results_display()

    def update_results_display(self):
        for option_name, votes in self.options.items():
            self.results_labels[option_name].config(text=f"{option_name}: {votes} votes")

    def reset_votes(self):
        if messagebox.askyesno("Reset Votes", "Are you sure you want to reset all votes?"):
            for option_name in self.options.keys():
                self.options[option_name] = 0
            self.update_results_display()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x500")
    app = VotingSystemApp(root)
    root.mainloop()
