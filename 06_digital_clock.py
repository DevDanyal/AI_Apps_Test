import tkinter as tk
import time

class DigitalClockApp:
    def __init__(self, master):
        self.master = master
        master.title("Digital Clock")
        master.geometry("400x100")
        master.resizable(False, False)

        # Time display label
        self.time_label = tk.Label(master, font=('calibri', 40, 'bold'), background='black', foreground='white')
        self.time_label.pack(expand=True, fill='both')

        self.update_time()

    def update_time(self):
        """Updates the time displayed on the label every second."""
        current_time = time.strftime('%I:%M:%S %p') # Format: 12-hour with AM/PM
        self.time_label.config(text=current_time)
        self.master.after(1000, self.update_time) # Call itself after 1000ms (1 second)

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalClockApp(root)
    root.mainloop()
