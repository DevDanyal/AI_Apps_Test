import tkinter as tk
from tkinter import messagebox
import time

class CountdownTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("400x300")

        self.time_left = 0
        self.timer_running = False

        # --- UI Elements ---
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        self.hour_label = tk.Label(self.input_frame, text="Hours:")
        self.hour_label.pack(side="left", padx=5)
        self.hour_entry = tk.Entry(self.input_frame, width=5)
        self.hour_entry.pack(side="left")
        self.hour_entry.insert(0, "0")

        self.minute_label = tk.Label(self.input_frame, text="Minutes:")
        self.minute_label.pack(side="left", padx=5)
        self.minute_entry = tk.Entry(self.input_frame, width=5)
        self.minute_entry.pack(side="left")
        self.minute_entry.insert(0, "0")

        self.second_label = tk.Label(self.input_frame, text="Seconds:")
        self.second_label.pack(side="left", padx=5)
        self.second_entry = tk.Entry(self.input_frame, width=5)
        self.second_entry.pack(side="left")
        self.second_entry.insert(0, "10")

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer, state="disabled")
        self.stop_button.pack(pady=5)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(pady=5)

        self.timer_label = tk.Label(root, text="", font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

    def start_timer(self):
        if self.timer_running:
            return
        
        try:
            hours = int(self.hour_entry.get())
            minutes = int(self.minute_entry.get())
            seconds = int(self.second_entry.get())
            self.time_left = hours * 3600 + minutes * 60 + seconds
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for time.")
            return

        if self.time_left <= 0:
            messagebox.showwarning("Invalid Time", "Please enter a positive time value.")
            return
            
        self.timer_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def reset_timer(self):
        self.stop_timer()
        self.time_left = 0
        self.timer_label.config(text="")
        self.hour_entry.delete(0, 'end')
        self.minute_entry.delete(0, 'end')
        self.second_entry.delete(0, 'end')
        self.hour_entry.insert(0, "0")
        self.minute_entry.insert(0, "0")
        self.second_entry.insert(0, "10")

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60

            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_str)
            
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.timer_label.config(text="00:00:00")
            messagebox.showinfo("Time's Up!", "The countdown has finished.")
            self.reset_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimerApp(root)
    root.mainloop()
