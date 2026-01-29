import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from datetime import datetime
import os
import csv

class AttendanceSystem:
    def __init__(self, master):
        self.master = master
        master.title("Attendance System")
        master.geometry("600x700")
        master.resizable(False, False)

        self.attendance_file = "attendance_records.csv"
        self.records = self.load_records()
        self.create_widgets()

    def create_widgets(self):
        # Frame for student/employee input
        input_frame = tk.Frame(self.master, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Name:").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        self.mark_present_button = tk.Button(input_frame, text="Mark Present", command=lambda: self.mark_attendance("Present"))
        self.mark_present_button.pack(side=tk.LEFT, padx=5)

        self.mark_absent_button = tk.Button(input_frame, text="Mark Absent", command=lambda: self.mark_attendance("Absent"))
        self.mark_absent_button.pack(side=tk.LEFT, padx=5)

        # Separator
        tk.Frame(self.master, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

        # Display records
        tk.Label(self.master, text="Attendance Records:").pack(anchor=tk.W, padx=10, pady=5)
        self.record_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled', width=70, height=25)
        self.record_display.pack(padx=10, pady=5)

        self.update_display()

        # Save and Clear Buttons
        button_frame = tk.Frame(self.master, padx=10, pady=10)
        button_frame.pack(fill=tk.X)

        self.save_button = tk.Button(button_frame, text="Save Records", command=self.save_records)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear All Records", command=self.clear_all_records)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def mark_attendance(self, status):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.records.append({"Name": name, "Status": status, "Timestamp": timestamp})
        self.update_display()
        self.name_entry.delete(0, tk.END)
        messagebox.showinfo("Attendance Marked", f"{name} marked as {status}.")

    def update_display(self):
        self.record_display.config(state='normal')
        self.record_display.delete(1.0, tk.END)
        if not self.records:
            self.record_display.insert(tk.END, "No attendance records yet.\n")
        else:
            # Display header
            self.record_display.insert(tk.END, f"{ 'Name':<20} {'Status':<10} {'Timestamp':<20}\n", "header")
            self.record_display.insert(tk.END, "-"*50 + "\n", "separator")
            for record in self.records:
                self.record_display.insert(tk.END, f"{record['Name']:<20} {record['Status']:<10} {record['Timestamp']:<20}\n")
        self.record_display.config(state='disabled')
        self.record_display.yview(tk.END)

        self.record_display.tag_config("header", font=("TkDefaultFont", 10, "bold"))
        self.record_display.tag_config("separator", foreground="gray")

    def load_records(self):
        if not os.path.exists(self.attendance_file):
            return []
        records = []
        with open(self.attendance_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                records.append(row)
        return records

    def save_records(self):
        if not self.records:
            messagebox.showinfo("Save Records", "No records to save.")
            return

        with open(self.attendance_file, mode='w', newline='') as file:
            fieldnames = ["Name", "Status", "Timestamp"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.records)
        messagebox.showinfo("Save Records", "Attendance records saved successfully.")

    def clear_all_records(self):
        if messagebox.askyesno("Clear Records", "Are you sure you want to clear all attendance records? This cannot be undone."):
            self.records = []
            self.save_records() # Also clears the file
            self.update_display()
            messagebox.showinfo("Records Cleared", "All attendance records have been cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()
