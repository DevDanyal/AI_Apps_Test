import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessingGameApp:
    def __init__(self, master):
        self.master = master
        master.title("Number Guessing Game")
        master.geometry("300x250")
        master.resizable(False, False)

        self.secret_number = 0
        self.attempts = 0
        self.min_range = 1
        self.max_range = 100

        # --- UI Elements ---
        main_frame = tk.Frame(master, padx=10, pady=10)
        main_frame.pack(expand=True, fill="both")

        self.instruction_label = tk.Label(main_frame, text=f"Guess a number between {self.min_range} and {self.max_range}", font=('arial', 12))
        self.instruction_label.pack(pady=10)

        self.guess_entry = tk.Entry(main_frame, font=('arial', 14), width=10)
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess()) # Allow pressing Enter to guess

        self.guess_button = tk.Button(main_frame, text="Guess", command=self.check_guess, font=('arial', 12, 'bold'), bg='lightblue')
        self.guess_button.pack(pady=5)

        self.message_label = tk.Label(main_frame, text="", font=('arial', 12, 'italic'))
        self.message_label.pack(pady=10)

        self.new_game_button = tk.Button(main_frame, text="New Game", command=self.start_new_game, font=('arial', 12, 'bold'), bg='lightgreen')
        self.new_game_button.pack(pady=5)
        self.new_game_button.config(state="disabled") # Disabled until a game ends

        self.start_new_game() # Start the first game automatically

    def start_new_game(self):
        """Starts a new guessing game."""
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.instruction_label.config(text=f"I'm thinking of a number between {self.min_range} and {self.max_range}")
        self.message_label.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state="normal")
        self.guess_button.config(state="normal")
        self.new_game_button.config(state="disabled")
        self.guess_entry.focus_set() # Set focus to the entry field

    def check_guess(self):
        """Checks the user's guess against the secret number."""
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1

            if guess < self.min_range or guess > self.max_range:
                self.message_label.config(text=f"Please guess a number between {self.min_range} and {self.max_range}.")
                return

            if guess < self.secret_number:
                self.message_label.config(text="Too low, try again!")
            elif guess > self.secret_number:
                self.message_label.config(text="Too high, try again!")
            else:
                self.message_label.config(text=f"Congratulations! You guessed it in {self.attempts} attempts!")
                self.guess_entry.config(state="disabled")
                self.guess_button.config(state="disabled")
                self.new_game_button.config(state="normal")

        except ValueError:
            self.message_label.config(text="Invalid input. Please enter a number.")
        self.guess_entry.delete(0, tk.END) # Clear entry after each guess

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGameApp(root)
    root.mainloop()
