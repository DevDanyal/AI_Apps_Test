import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class FileBackupToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple File Backup Tool")

        self.source_folder = ""
        self.destination_folder = ""

        self.create_widgets()

    def create_widgets(self):
        # Source Folder Selection
        self.source_frame = tk.LabelFrame(self.root, text="Source Folder", padx=10, pady=10)
        self.source_frame.pack(pady=10, padx=10, fill=tk.X)

        self.source_label = tk.Label(self.source_frame, text="No folder selected", wraplength=400, justify=tk.LEFT)
        self.source_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.source_button = tk.Button(self.source_frame, text="Select Source", command=self.select_source_folder)
        self.source_button.pack(side=tk.RIGHT)

        # Destination Folder Selection
        self.destination_frame = tk.LabelFrame(self.root, text="Destination Folder", padx=10, pady=10)
        self.destination_frame.pack(pady=10, padx=10, fill=tk.X)

        self.destination_label = tk.Label(self.destination_frame, text="No folder selected", wraplength=400, justify=tk.LEFT)
        self.destination_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.destination_button = tk.Button(self.destination_frame, text="Select Destination", command=self.select_destination_folder)
        self.destination_button.pack(side=tk.RIGHT)

        # Backup Button
        self.backup_button = tk.Button(self.root, text="Backup Files", command=self.backup_files,
                                       font=("Arial", 14, "bold"), bg="green", fg="white")
        self.backup_button.pack(pady=20)

        # Status Display
        self.status_text = tk.Text(self.root, height=10, width=60, state=tk.DISABLED)
        self.status_text.pack(pady=10, padx=10)

    def select_source_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.source_folder = folder_selected
            self.source_label.config(text=self.source_folder)
            self.update_status(f"Source folder selected: {self.source_folder}")

    def select_destination_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.destination_folder = folder_selected
            self.destination_label.config(text=self.destination_folder)
            self.update_status(f"Destination folder selected: {self.destination_folder}")

    def backup_files(self):
        if not self.source_folder:
            messagebox.showerror("Error", "Please select a source folder.")
            return
        if not self.destination_folder:
            messagebox.showerror("Error", "Please select a destination folder.")
            return
        if not os.path.exists(self.destination_folder):
            os.makedirs(self.destination_folder)
            self.update_status(f"Created destination folder: {self.destination_folder}")

        self.update_status("\nStarting backup...")
        try:
            for item in os.listdir(self.source_folder):
                source_path = os.path.join(self.source_folder, item)
                destination_path = os.path.join(self.destination_folder, item)

                if os.path.isfile(source_path):
                    shutil.copy2(source_path, destination_path)
                    self.update_status(f"Backed up file: {item}")
                elif os.path.isdir(source_path):
                    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                    self.update_status(f"Backed up directory: {item}")
            self.update_status("\nBackup complete!")
            messagebox.showinfo("Backup", "Files backed up successfully!")
        except Exception as e:
            self.update_status(f"\nError during backup: {e}")
            messagebox.showerror("Backup Error", f"An error occurred during backup: {e}")

    def update_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)  # Auto-scroll to the end
        self.status_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    app = FileBackupToolApp(root)
    root.mainloop()
