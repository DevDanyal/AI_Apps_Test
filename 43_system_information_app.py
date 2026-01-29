
import tkinter as tk
from tkinter import messagebox
import psutil
import platform
import os

class SystemInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Information")

        self.create_widgets()
        self.update_system_info()
        self.schedule_update()

    def create_widgets(self):
        # OS Information
        self.os_frame = tk.LabelFrame(self.root, text="Operating System", padx=10, pady=10)
        self.os_frame.pack(pady=10, padx=10, fill=tk.X)
        self.os_label = tk.Label(self.os_frame, text="", justify=tk.LEFT)
        self.os_label.pack(fill=tk.X)

        # CPU Information
        self.cpu_frame = tk.LabelFrame(self.root, text="CPU Information", padx=10, pady=10)
        self.cpu_frame.pack(pady=10, padx=10, fill=tk.X)
        self.cpu_count_label = tk.Label(self.cpu_frame, text="", justify=tk.LEFT)
        self.cpu_count_label.pack(fill=tk.X)
        self.cpu_usage_label = tk.Label(self.cpu_frame, text="", justify=tk.LEFT)
        self.cpu_usage_label.pack(fill=tk.X)

        # Memory Information
        self.memory_frame = tk.LabelFrame(self.root, text="Memory Information", padx=10, pady=10)
        self.memory_frame.pack(pady=10, padx=10, fill=tk.X)
        self.total_memory_label = tk.Label(self.memory_frame, text="", justify=tk.LEFT)
        self.total_memory_label.pack(fill=tk.X)
        self.available_memory_label = tk.Label(self.memory_frame, text="", justify=tk.LEFT)
        self.available_memory_label.pack(fill=tk.X)
        self.used_memory_label = tk.Label(self.memory_frame, text="", justify=tk.LEFT)
        self.used_memory_label.pack(fill=tk.X)
        self.memory_percent_label = tk.Label(self.memory_frame, text="", justify=tk.LEFT)
        self.memory_percent_label.pack(fill=tk.X)

        # Refresh Button
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.update_system_info)
        self.refresh_button.pack(pady=10)

    def update_system_info(self):
        try:
            # OS Info
            os_name = platform.system()
            os_release = platform.release()
            os_version = platform.version()
            self.os_label.config(text=f"OS: {os_name}\nRelease: {os_release}\nVersion: {os_version}")

            # CPU Info
            cpu_physical_cores = psutil.cpu_count(logical=False)
            cpu_logical_cores = psutil.cpu_count(logical=True)
            cpu_usage = psutil.cpu_percent(interval=1) # interval for a non-blocking call
            self.cpu_count_label.config(text=f"Physical Cores: {cpu_physical_cores}\nLogical Cores: {cpu_logical_cores}")
            self.cpu_usage_label.config(text=f"CPU Usage: {cpu_usage}%")

            # Memory Info
            memory = psutil.virtual_memory()
            total_gb = round(memory.total / (1024**3), 2)
            available_gb = round(memory.available / (1024**3), 2)
            used_gb = round(memory.used / (1024**3), 2)
            self.total_memory_label.config(text=f"Total Memory: {total_gb} GB")
            self.available_memory_label.config(text=f"Available Memory: {available_gb} GB")
            self.used_memory_label.config(text=f"Used Memory: {used_gb} GB")
            self.memory_percent_label.config(text=f"Memory Usage: {memory.percent}%")

        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve system information. Please ensure 'psutil' is installed.\nError: {e}")

    def schedule_update(self):
        # Update every 5 seconds
        self.root.after(5000, self.update_system_info)
        self.root.after(5000, self.schedule_update) # Reschedule itself

if __name__ == "__main__":
    try:
        # Initial check for psutil
        psutil.cpu_percent(interval=None)
    except Exception:
        messagebox.showerror("Error", "The 'psutil' library is not installed. Please install it using: pip install psutil")
    else:
        root = tk.Tk()
        app = SystemInfoApp(root)
        root.mainloop()
