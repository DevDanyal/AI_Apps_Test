import tkinter as tk
from tkinter import messagebox
import calendar
from datetime import datetime

class CalendarApp:
    def __init__(self, master):
        self.master = master
        master.title("Calendar App")
        master.geometry("400x450")
        master.resizable(False, False)

        self.year = datetime.now().year
        self.month = datetime.now().month

        self.create_widgets()
        self.display_calendar()

    def create_widgets(self):
        # Month and Year Display Frame
        header_frame = tk.Frame(self.master)
        header_frame.pack(pady=10)

        self.prev_button = tk.Button(header_frame, text="<", command=self.prev_month)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.month_year_label = tk.Label(header_frame, text="", font=("Arial", 16, "bold"))
        self.month_year_label.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(header_frame, text=">", command=self.next_month)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Day Names (Mon, Tue, etc.)
        day_names_frame = tk.Frame(self.master)
        day_names_frame.pack()
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days_of_week):
            tk.Label(day_names_frame, text=day, width=5, font=("Arial", 10, "bold")).grid(row=0, column=i)

        # Calendar Grid Frame
        self.calendar_frame = tk.Frame(self.master)
        self.calendar_frame.pack()

    def display_calendar(self):
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.Calendar()
        month_days = cal.monthdayscalendar(self.year, self.month)

        month_name = calendar.month_name[self.month]
        self.month_year_label.config(text=f"{month_name} {self.year}")

        for week_idx, week in enumerate(month_days):
            for day_idx, day in enumerate(week):
                day_label = tk.Label(self.calendar_frame, text=str(day) if day != 0 else "", width=5, height=2, bd=1, relief="solid")
                day_label.grid(row=week_idx, column=day_idx, padx=1, pady=1)

                if day == 0:
                    day_label.config(bg="lightgray")
                elif day == datetime.now().day and self.month == datetime.now().month and self.year == datetime.now().year:
                    day_label.config(bg="lightblue", fg="blue", font=("Arial", 10, "bold")) # Highlight current day

                # Example of highlighting a specific date (e.g., 15th of current month)
                if day == 15 and self.month == datetime.now().month and self.year == datetime.now().year:
                     day_label.config(bg="lightgreen", fg="darkgreen", font=("Arial", 10, "bold"))


    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.display_calendar()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.display_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
