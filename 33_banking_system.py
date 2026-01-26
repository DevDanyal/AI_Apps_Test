import tkinter as tk
from tkinter import messagebox

class BankingSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Banking System")
        self.root.geometry("400x300")

        self.balance = 0.0

        # --- UI Elements ---
        self.balance_display_label = tk.Label(root, text=f"Current Balance: ${self.balance:.2f}", font=("Helvetica", 16))
        self.balance_display_label.pack(pady=20)

        self.amount_label = tk.Label(root, text="Enter Amount:")
        self.amount_label.pack(pady=5)

        self.amount_entry = tk.Entry(root, width=30)
        self.amount_entry.pack(pady=5)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.deposit_button = tk.Button(self.button_frame, text="Deposit", command=self.deposit)
        self.deposit_button.pack(side=tk.LEFT, padx=10)

        self.withdraw_button = tk.Button(self.button_frame, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack(side=tk.LEFT, padx=10)

        self.message_label = tk.Label(root, text="", fg="blue")
        self.message_label.pack(pady=10)

        self.update_balance_display()

    def update_balance_display(self):
        self.balance_display_label.config(text=f"Current Balance: ${self.balance:.2f}")

    def get_amount_input(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Invalid Amount", "Amount must be positive.")
                return None
            return amount
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")
            return None
        finally:
            self.amount_entry.delete(0, tk.END)

    def deposit(self):
        amount = self.get_amount_input()
        if amount is not None:
            self.balance += amount
            self.update_balance_display()
            self.message_label.config(text=f"Deposited ${amount:.2f} successfully.", fg="green")

    def withdraw(self):
        amount = self.get_amount_input()
        if amount is not None:
            if self.balance >= amount:
                self.balance -= amount
                self.update_balance_display()
                self.message_label.config(text=f"Withdrew ${amount:.2f} successfully.", fg="green")
            else:
                self.message_label.config(text="Error: Insufficient funds.", fg="red")
                messagebox.showerror("Insufficient Funds", "You do not have enough money to withdraw this amount.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystemApp(root)
    root.mainloop()
