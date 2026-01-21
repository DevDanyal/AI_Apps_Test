import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")
        master.geometry("400x350")
        master.resizable(False, False)

        # --- Variables ---
        self.length_var = tk.IntVar(value=12)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.password_var = tk.StringVar()

        # --- UI Elements ---

        # Options Frame
        options_frame = tk.LabelFrame(master, text="Password Options", padx=10, pady=10)
        options_frame.pack(padx=10, pady=10, fill="x")

        # Length
        tk.Label(options_frame, text="Password Length:").grid(row=0, column=0, sticky="w", pady=2)
        tk.Spinbox(options_frame, from_=4, to_=64, textvariable=self.length_var, width=5).grid(row=0, column=1, sticky="w")

        # Character Types
        tk.Checkbutton(options_frame, text="Include Uppercase (A-Z)", variable=self.uppercase_var).grid(row=1, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(options_frame, text="Include Lowercase (a-z)", variable=self.lowercase_var).grid(row=2, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(options_frame, text="Include Numbers (0-9)", variable=self.numbers_var).grid(row=3, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(options_frame, text="Include Symbols (!@#...)", variable=self.symbols_var).grid(row=4, column=0, columnspan=2, sticky="w")

        # Generate Button
        generate_button = tk.Button(master, text="Generate Password", command=self.generate_password, font=('arial', 12, 'bold'), bg='lightblue')
        generate_button.pack(pady=10)

        # Result Frame
        result_frame = tk.LabelFrame(master, text="Generated Password", padx=10, pady=10)
        result_frame.pack(padx=10, pady=10, fill="x")

        password_entry = tk.Entry(result_frame, textvariable=self.password_var, font=('arial', 14), bd=0, state="readonly")
        password_entry.pack(side=tk.LEFT, fill="x", expand=True)

        copy_button = tk.Button(result_frame, text="Copy", command=self.copy_to_clipboard)
        copy_button.pack(side=tk.LEFT, padx=5)

    def generate_password(self):
        """Generates a password based on the selected criteria."""
        length = self.length_var.get()
        char_sets = []
        password_chars = []

        if self.uppercase_var.get():
            char_sets.append(string.ascii_uppercase)
            password_chars.append(random.choice(string.ascii_uppercase))
        if self.lowercase_var.get():
            char_sets.append(string.ascii_lowercase)
            password_chars.append(random.choice(string.ascii_lowercase))
        if self.numbers_var.get():
            char_sets.append(string.digits)
            password_chars.append(random.choice(string.digits))
        if self.symbols_var.get():
            char_sets.append(string.punctuation)
            password_chars.append(random.choice(string.punctuation))

        if not char_sets:
            messagebox.showwarning("Warning", "You must select at least one character type.")
            return

        if length < len(password_chars):
            messagebox.showwarning("Warning", f"Length must be at least {len(password_chars)} to include all selected character types.")
            return

        all_chars = "".join(char_sets)
        
        remaining_length = length - len(password_chars)
        for _ in range(remaining_length):
            password_chars.append(random.choice(all_chars))

        random.shuffle(password_chars)
        
        final_password = "".join(password_chars)
        self.password_var.set(final_password)

    def copy_to_clipboard(self):
        """Copies the generated password to the clipboard."""
        password = self.password_var.get()
        if password:
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
