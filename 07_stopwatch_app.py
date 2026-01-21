import tkinter as tk
import time

class StopwatchApp:
    def __init__(self, master):
        self.master = master
        master.title("Stopwatch")
        master.geometry("400x200")
        master.resizable(False, False)

        self.running = False
        self.start_time = 0.0
        self.elapsed_time = 0.0

        # --- UI Elements ---

        # Time display
        self.time_label = tk.Label(master, text="00:00:00.00", font=('calibri', 40, 'bold'), background='black', foreground='white')
        self.time_label.pack(expand=True, fill='both', pady=10, padx=10)

        # Button frame
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.start_pause_button = tk.Button(button_frame, text="Start", width=10, command=self.start_pause, font=('arial', 12, 'bold'), bg='lightgreen')
        self.start_pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset", width=10, command=self.reset, font=('arial', 12, 'bold'), bg='orange')
        self.reset_button.pack(side=tk.LEFT, padx=5)


    def start_pause(self):
        """Toggles the stopwatch between running and paused states."""
        if self.running: # Pause
            self.running = False
            self.elapsed_time += time.time() - self.start_time
            self.start_pause_button.config(text="Start", bg='lightgreen')
        else: # Start/Resume
            self.running = True
            self.start_time = time.time()
            self.start_pause_button.config(text="Pause", bg='red')
            self.update_time()

    def reset(self):
        """Resets the stopwatch."""
        self.running = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.time_label.config(text="00:00:00.00")
        self.start_pause_button.config(text="Start", bg='lightgreen')

    def update_time(self):
        """Updates the time display label."""
        if self.running:
            current_elapsed = self.elapsed_time + (time.time() - self.start_time)
            
            # Format time
            minutes, seconds = divmod(current_elapsed, 60)
            hours, minutes = divmod(minutes, 60)
            
            time_string = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int((current_elapsed % 1) * 100):02}"
            self.time_label.config(text=time_string)
            
            # Call itself after 50ms
            self.master.after(50, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
