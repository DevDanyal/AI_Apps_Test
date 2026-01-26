import tkinter as tk
from tkinter import messagebox
import datetime
import time
import winsound

class AlarmClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("400x300")

        self.alarm_time = None
        self.alarm_set = False

        # --- UI Elements ---
        self.current_time_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.current_time_label.pack(pady=20)

        self.alarm_frame = tk.Frame(root)
        self.alarm_frame.pack(pady=10)

        self.hour_label = tk.Label(self.alarm_frame, text="Hour:")
        self.hour_label.pack(side="left")
        self.hour_spinbox = tk.Spinbox(self.alarm_frame, from_=0, to=23, width=5, format="%02.0f")
        self.hour_spinbox.pack(side="left")

        self.minute_label = tk.Label(self.alarm_frame, text="Minute:")
        self.minute_label.pack(side="left", padx=(10, 0))
        self.minute_spinbox = tk.Spinbox(self.alarm_frame, from_=0, to=59, width=5, format="%02.0f")
        self.minute_spinbox.pack(side="left")

        self.set_alarm_button = tk.Button(root, text="Set Alarm", command=self.set_alarm)
        self.set_alarm_button.pack(pady=10)
        
        self.stop_alarm_button = tk.Button(root, text="Stop Alarm", command=self.stop_alarm, state="disabled")
        self.stop_alarm_button.pack(pady=5)

        self.alarm_status_label = tk.Label(root, text="No alarm set")
        self.alarm_status_label.pack(pady=10)

        self.update_time()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.current_time_label.config(text=current_time)
        self.check_alarm()
        self.root.after(1000, self.update_time)

    def set_alarm(self):
        try:
            hour = int(self.hour_spinbox.get())
            minute = int(self.minute_spinbox.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for hour and minute.")
            return

        self.alarm_time = f"{hour:02d}:{minute:02d}"
        self.alarm_set = True
        self.alarm_status_label.config(text=f"Alarm set for {self.alarm_time}")
        self.set_alarm_button.config(state="disabled")
        self.stop_alarm_button.config(state="normal")
        messagebox.showinfo("Alarm Set", f"Alarm is set for {self.alarm_time}")


    def stop_alarm(self):
        self.alarm_set = False
        self.alarm_status_label.config(text="No alarm set")
        self.set_alarm_button.config(state="normal")
        self.stop_alarm_button.config(state="disabled")
        winsound.PlaySound(None, winsound.SND_PURGE) # Stop any playing sound

    def check_alarm(self):
        if self.alarm_set:
            current_time = datetime.datetime.now().strftime("%H:%M")
            if current_time == self.alarm_time:
                self.trigger_alarm()

    def trigger_alarm(self):
        messagebox.showinfo("Alarm", "Time's up!")
        # Play the alarm sound in a loop
        winsound.PlaySound("alarm.wav", winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)


if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClockApp(root)
    root.mainloop()
