import tkinter as tk
from tkinter import filedialog, messagebox

class NotepadApp:
    def __init__(self, master):
        self.master = master
        master.title("Untitled - Notepad")
        master.geometry("800x600")

        self.current_file = None

        # Text Area
        self.text_area = tk.Text(master, wrap='word', font=('Arial', 12))
        self.text_area.pack(expand=True, fill='both')

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        # Menu Bar
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As...", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Clear Text", command=self.clear_text)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)

    def new_file(self):
        """Clears the text area and sets the title to 'Untitled'."""
        self.text_area.delete(1.0, tk.END)
        self.master.title("Untitled - Notepad")
        self.current_file = None

    def open_file(self):
        """Opens a file dialog, reads the selected file, and displays its content."""
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("Text Files", "*.txt"),
                                                          ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, file.read())
                self.current_file = file_path
                self.master.title(f"{file_path} - Notepad")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        """Saves the current file, or calls save_file_as if it's a new file."""
        if self.current_file:
            try:
                with open(self.current_file, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Opens a save file dialog and saves the content to the chosen file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"),
                                                            ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.current_file = file_path
                self.master.title(f"{file_path} - Notepad")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def clear_text(self):
        """Clears all text from the text area."""
        self.text_area.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()
