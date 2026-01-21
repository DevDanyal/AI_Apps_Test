import tkinter as tk
from tkinter import messagebox

class LoginSystemApp:
    def __init__(self, master):
        self.master = master
        master.title("Login System")
        master.geometry("300x150")
        master.resizable(False, False)

        # Hardcoded credentials for demonstration
        self.VALID_USERNAME = "admin"
        self.VALID_PASSWORD = "password123"

        # --- UI Elements ---
        self.main_frame = tk.Frame(master, padx=10, pady=10)
        self.main_frame.pack(expand=True, fill="both")

        # Username
        tk.Label(self.main_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.grid(row=0, column=1, sticky="ew")

        # Password
        tk.Label(self.main_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew")

        # Login Button
        self.login_button = tk.Button(self.main_frame, text="Login", command=self.validate_login, font=('arial', 10, 'bold'))
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Configure column weights for resizing
        self.main_frame.columnconfigure(1, weight=1)

    def validate_login(self):
        """Validates the entered username and password."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == self.VALID_USERNAME and password == self.VALID_PASSWORD:
            messagebox.showinfo("Login Successful", "Welcome, admin!")
            # Here you would typically open the main application window
            # For this example, we'll just disable the login fields
            self.username_entry.config(state="disabled")
            self.password_entry.config(state="disabled")
            self.login_button.config(state="disabled")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            # Clear the password field after a failed attempt
            self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSystemApp(root)
    root.mainloop()
