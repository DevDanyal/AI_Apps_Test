import tkinter as tk
from tkinter import messagebox

class EmailSlicerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Slicer")
        self.root.geometry("400x250")

        # --- UI Elements ---
        self.email_label = tk.Label(root, text="Enter Email Address:")
        self.email_label.pack(pady=10)

        self.email_entry = tk.Entry(root, width=40)
        self.email_entry.pack(pady=5)

        self.slice_button = tk.Button(root, text="Slice Email", command=self.slice_email)
        self.slice_button.pack(pady=10)

        self.username_label = tk.Label(root, text="Username: ")
        self.username_label.pack(pady=5)

        self.domain_label = tk.Label(root, text="Domain: ")
        self.domain_label.pack(pady=5)

    def slice_email(self):
        email = self.email_entry.get().strip()

        if not email:
            messagebox.showwarning("Input Error", "Please enter an email address.")
            return

        if "@" not in email:
            messagebox.showerror("Invalid Email", "Email address must contain '@' symbol.")
            self.username_label.config(text="Username: ")
            self.domain_label.config(text="Domain: ")
            return

        try:
            username, domain = email.split('@')
            self.username_label.config(text=f"Username: {username}")
            self.domain_label.config(text=f"Domain: {domain}")
        except ValueError:
            messagebox.showerror("Invalid Email", "Invalid email format.")
            self.username_label.config(text="Username: ")
            self.domain_label.config(text="Domain: ")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSlicerApp(root)
    root.mainloop()
