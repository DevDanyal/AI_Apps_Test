import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from datetime import datetime
import os
import csv
from collections import defaultdict

class ExpenseTracker:
    def __init__(self, master):
        self.master = master
        master.title("Expense Tracker")
        master.geometry("700x700")
        master.resizable(False, False)

        self.expense_file = "expenses.csv"
        self.expenses = self.load_expenses() # List of dictionaries
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Input Frame
        input_frame = tk.Frame(self.master, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.amount_entry = tk.Entry(input_frame, width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.category_entry = tk.Entry(input_frame, width=20)
        self.category_entry.grid(row=1, column=1, padx=5, pady=2)

        self.add_button = tk.Button(input_frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Separator
        tk.Frame(self.master, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

        # Recent Expenses Display
        tk.Label(self.master, text="Recent Expenses:").pack(anchor=tk.W, padx=10, pady=5)
        self.recent_expenses_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled', width=80, height=15)
        self.recent_expenses_display.pack(padx=10, pady=5)

        # Separator
        tk.Frame(self.master, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

        # Summary Display
        tk.Label(self.master, text="Expense Summary:").pack(anchor=tk.W, padx=10, pady=5)
        self.summary_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled', width=80, height=10)
        self.summary_display.pack(padx=10, pady=5)

        # Save and Clear Buttons
        button_frame_bottom = tk.Frame(self.master, padx=10, pady=10)
        button_frame_bottom.pack(fill=tk.X)

        self.save_button = tk.Button(button_frame_bottom, text="Save Expenses", command=self.save_expenses)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame_bottom, text="Clear All Expenses", command=self.clear_all_expenses)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get().strip()

            if not category:
                messagebox.showwarning("Input Error", "Please enter a category.")
                return
            if amount <= 0:
                messagebox.showwarning("Input Error", "Amount must be greater than zero.")
                return

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.expenses.append({"Amount": amount, "Category": category, "Timestamp": timestamp})
            self.update_display()
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            messagebox.showinfo("Expense Added", f"Expense of ${amount:.2f} in '{category}' added.")

        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid amount (number).")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def update_display(self):
        self.display_recent_expenses()
        self.display_summary()

    def display_recent_expenses(self):
        self.recent_expenses_display.config(state='normal')
        self.recent_expenses_display.delete(1.0, tk.END)

        if not self.expenses:
            self.recent_expenses_display.insert(tk.END, "No expenses recorded yet.\n")
        else:
            self.recent_expenses_display.insert(tk.END, f"{ 'Amount':<10} {'Category':<20} {'Date':<20}\n", "header")
            self.recent_expenses_display.insert(tk.END, "-"*55 + "\n", "separator")
            for expense in reversed(self.expenses[-10:]): # Display last 10 expenses
                self.recent_expenses_display.insert(tk.END, f"${expense['Amount']:<9.2f} {expense['Category']:<20} {expense['Timestamp']:<20}\n")
        self.recent_expenses_display.config(state='disabled')
        self.recent_expenses_display.yview(tk.END)
        self.recent_expenses_display.tag_config("header", font=("TkDefaultFont", 10, "bold"))
        self.recent_expenses_display.tag_config("separator", foreground="gray")

    def display_summary(self):
        self.summary_display.config(state='normal')
        self.summary_display.delete(1.0, tk.END)

        if not self.expenses:
            self.summary_display.insert(tk.END, "No expenses to summarize.\n")
            self.summary_display.config(state='disabled')
            return

        total_expenses = sum(exp['Amount'] for exp in self.expenses)
        self.summary_display.insert(tk.END, f"Total Expenses: ${total_expenses:.2f}\n\n", "total_header")

        expenses_by_category = defaultdict(float)
        for expense in self.expenses:
            expenses_by_category[expense['Category']] += expense['Amount']

        self.summary_display.insert(tk.END, "Expenses by Category:\n", "category_header")
        for category, amount in expenses_by_category.items():
            self.summary_display.insert(tk.END, f"- {category}: ${amount:.2f}\n")
        
        self.summary_display.config(state='disabled')
        self.summary_display.tag_config("total_header", font=("TkDefaultFont", 12, "bold"), foreground="blue")
        self.summary_display.tag_config("category_header", font=("TkDefaultFont", 11, "bold"), foreground="darkgreen")


    def load_expenses(self):
        if not os.path.exists(self.expense_file):
            return []
        expenses = []
        with open(self.expense_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert amount back to float
                row['Amount'] = float(row['Amount'])
                expenses.append(row)
        return expenses

    def save_expenses(self):
        if not self.expenses:
            messagebox.showinfo("Save Expenses", "No expenses to save.")
            return

        with open(self.expense_file, mode='w', newline='') as file:
            fieldnames = ["Amount", "Category", "Timestamp"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.expenses)
        messagebox.showinfo("Save Expenses", "Expense records saved successfully.")

    def clear_all_expenses(self):
        if messagebox.askyesno("Clear Expenses", "Are you sure you want to clear all expense records? This cannot be undone."):
            self.expenses = []
            self.save_expenses() # Also clears the file content
            self.update_display()
            messagebox.showinfo("Records Cleared", "All expense records have been cleared.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
