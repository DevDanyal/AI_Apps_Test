import tkinter as tk
from tkinter import messagebox
import re

class PasswordCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("400x350")

        # --- UI Elements ---
        self.password_label = tk.Label(root, text="Enter Password:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(root, width=40, show="*") # show="*" hides password input
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<KeyRelease>", self.check_strength_live)

        self.check_button = tk.Button(root, text="Check Strength", command=self.check_strength)
        self.check_button.pack(pady=10)

        self.strength_label = tk.Label(root, text="Strength: ", font=("Helvetica", 12, "bold"))
        self.strength_label.pack(pady=5)

        self.criteria_frame = tk.LabelFrame(root, text="Criteria Met")
        self.criteria_frame.pack(pady=10, padx=10, fill=tk.X)

        self.length_criteria = tk.Label(self.criteria_frame, text="- At least 8 characters")
        self.length_criteria.pack(anchor="w")
        self.uppercase_criteria = tk.Label(self.criteria_frame, text="- Contains uppercase letters")
        self.uppercase_criteria.pack(anchor="w")
        self.lowercase_criteria = tk.Label(self.criteria_frame, text="- Contains lowercase letters")
        self.lowercase_criteria.pack(anchor="w")
        self.digit_criteria = tk.Label(self.criteria_frame, text="- Contains numbers")
        self.digit_criteria.pack(anchor="w")
        self.special_criteria = tk.Label(self.criteria_frame, text="- Contains special characters")
        self.special_criteria.pack(anchor="w")

    def reset_criteria_colors(self):
        for widget in self.criteria_frame.winfo_children():
            widget.config(fg="black")

    def update_criteria_color(self, label, met):
        if met:
            label.config(fg="green")
        else:
            label.config(fg="red")

    def check_strength_live(self, event):
        self.check_strength()

    def check_strength(self):
        password = self.password_entry.get()
        self.reset_criteria_colors()

        if not password:
            self.strength_label.config(text="Strength: Empty", fg="gray")
            return

        score = 0
        
        # Length check
        has_length = len(password) >= 8
        self.update_criteria_color(self.length_criteria, has_length)
        if has_length: score += 1

        # Uppercase check
        has_uppercase = bool(re.search(r'[A-Z]', password))
        self.update_criteria_color(self.uppercase_criteria, has_uppercase)
        if has_uppercase: score += 1

        # Lowercase check
        has_lowercase = bool(re.search(r'[a-z]', password))
        self.update_criteria_color(self.lowercase_criteria, has_lowercase)
        if has_lowercase: score += 1

        # Digit check
        has_digit = bool(re.search(r'\d', password))
        self.update_criteria_color(self.digit_criteria, has_digit)
        if has_digit: score += 1

        # Special character check
        has_special = bool(re.search(r'[^A-Za-z0-9]', password))
        self.update_criteria_color(self.special_criteria, has_special)
        if has_special: score += 1

        # Determine overall strength
        if score == 5:
            strength_text = "Very Strong"
            color = "green"
        elif score == 4:
            strength_text = "Strong"
            color = "forestgreen"
        elif score == 3:
            strength_text = "Moderate"
            color = "orange"
        elif score == 2:
            strength_text = "Weak"
            color = "darkorange"
        else:
            strength_text = "Very Weak"
            color = "red"
        
        self.strength_label.config(text=f"Strength: {strength_text}", fg=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()
