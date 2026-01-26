import tkinter as tk
from tkinter import filedialog

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic File Explorer")
        self.root.geometry("400x200")

        self.label = tk.Label(root, text="No file selected", wraplength=380)
        self.label.pack(pady=20)

        self.select_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            initialdir="/",
            title="Select a File",
            filetypes=(
                ("All files", "*.*"),
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("Image files", "*.png *.jpg *.jpeg *.gif")
            )
        )
        if file_path:
            self.label.config(text=f"Selected File: {file_path}")
        else:
            self.label.config(text="No file selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()
