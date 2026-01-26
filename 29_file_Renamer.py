import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer Tool")
        self.root.geometry("700x500")

        self.directory_path = tk.StringVar()
        self.rename_pattern = tk.StringVar()
        self.rename_pattern.set("{num}_{name}{ext}") # Default pattern
        
        # --- UI Elements ---
        # Directory Selection
        self.dir_frame = tk.Frame(root)
        self.dir_frame.pack(pady=10, fill=tk.X, padx=10)

        self.dir_label = tk.Label(self.dir_frame, text="Selected Directory:")
        self.dir_label.pack(side=tk.LEFT)
        self.dir_entry = tk.Entry(self.dir_frame, textvariable=self.directory_path, state="readonly", width=50)
        self.dir_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.browse_button = tk.Button(self.dir_frame, text="Browse", command=self.browse_directory)
        self.browse_button.pack(side=tk.LEFT)

        # Rename Pattern Input
        self.pattern_frame = tk.Frame(root)
        self.pattern_frame.pack(pady=5, fill=tk.X, padx=10)

        self.pattern_label = tk.Label(self.pattern_frame, text="Rename Pattern:")
        self.pattern_label.pack(side=tk.LEFT)
        self.pattern_entry = tk.Entry(self.pattern_frame, textvariable=self.rename_pattern, width=50)
        self.pattern_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.pattern_entry.bind("<KeyRelease>", self.preview_rename) # Live preview

        # Preview Listbox
        self.preview_frame = tk.LabelFrame(root, text="Rename Preview (Original -> New)")
        self.preview_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        self.preview_listbox = tk.Listbox(self.preview_frame, width=80, height=15)
        self.preview_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.scrollbar = ttk.Scrollbar(self.preview_frame, orient="vertical", command=self.preview_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_listbox.config(yscrollcommand=self.scrollbar.set)

        # Rename Button
        self.rename_button = tk.Button(root, text="Perform Rename", command=self.perform_rename, state="disabled")
        self.rename_button.pack(pady=10)
        
        # Instructions
        self.instructions_label = tk.Label(root, text="Use {num} for sequence, {name} for original name, {ext} for extension. E.g., {num}_{name}{ext}")
        self.instructions_label.pack(pady=5)

    def browse_directory(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.directory_path.set(selected_directory)
            self.preview_rename()

    def get_files_in_directory(self):
        files = []
        if self.directory_path.get() and os.path.isdir(self.directory_path.get()):
            for item in os.listdir(self.directory_path.get()):
                if os.path.isfile(os.path.join(self.directory_path.get(), item)):
                    files.append(item)
        return sorted(files) # Sort for consistent numbering

    def preview_rename(self, event=None):
        self.preview_listbox.delete(0, tk.END)
        files = self.get_files_in_directory()
        pattern = self.rename_pattern.get()

        if not files or not pattern:
            self.rename_button.config(state="disabled")
            return

        valid_preview = True
        preview_names = []
        for i, original_name in enumerate(files):
            name_part, ext_part = os.path.splitext(original_name)
            
            try:
                new_name = pattern.format(num=i+1, name=name_part, ext=ext_part)
                if new_name == original_name:
                    valid_preview = False # No change, might indicate issue or no need to rename
                preview_names.append(new_name)
                self.preview_listbox.insert(tk.END, f"{original_name} -> {new_name}")
            except KeyError:
                self.preview_listbox.insert(tk.END, f"Error: Invalid pattern placeholder in '{pattern}'")
                valid_preview = False
                break
        
        # Check for duplicate new names
        if len(preview_names) != len(set(preview_names)):
            messagebox.showwarning("Duplicate Names", "The renaming pattern will result in duplicate filenames. Please adjust the pattern.")
            valid_preview = False
            
        self.rename_button.config(state="normal" if valid_preview else "disabled")

    def perform_rename(self):
        files = self.get_files_in_directory()
        pattern = self.rename_pattern.get()
        directory = self.directory_path.get()

        if not messagebox.askyesno("Confirm Rename", "Are you sure you want to rename these files? This action cannot be undone."):
            return

        renamed_count = 0
        for i, original_name in enumerate(files):
            name_part, ext_part = os.path.splitext(original_name)
            new_name = pattern.format(num=i+1, name=name_part, ext=ext_part)
            
            original_path = os.path.join(directory, original_name)
            new_path = os.path.join(directory, new_name)

            try:
                if original_path != new_path: # Only rename if name changes
                    os.rename(original_path, new_path)
                    renamed_count += 1
            except OSError as e:
                messagebox.showerror("Rename Error", f"Could not rename '{original_name}' to '{new_name}': {e}")
                continue
        
        messagebox.showinfo("Rename Complete", f"Successfully renamed {renamed_count} files.")
        self.preview_rename() # Refresh preview after renaming

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
