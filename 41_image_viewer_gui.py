
import tkinter as tk
from tkinter import filedialog, messagebox
try:
    from PIL import Image, ImageTk
except ImportError:
    messagebox.showerror("Error", "Pillow library not found. Please install it using: pip install Pillow")
import os

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.image_files = []
        self.current_image_index = -1

        # Frame for controls
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10)

        self.select_folder_button = tk.Button(self.control_frame, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = tk.Button(self.control_frame, text="<< Previous", command=self.show_previous_image, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.control_frame, text="Next >>", command=self.show_next_image, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Image display
        self.image_label = tk.Label(root)
        self.image_label.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.filename_label = tk.Label(root, text="")
        self.filename_label.pack()

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_files = self.load_images_from_folder(folder_path)
            if self.image_files:
                self.current_image_index = 0
                self.show_image()
            else:
                messagebox.showinfo("No Images", "No image files found in the selected folder.")
                self.current_image_index = -1
                self.image_label.config(image=None)
                self.filename_label.config(text="")
            self.update_button_states()

    def load_images_from_folder(self, folder_path):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico']
        files = []
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                files.append(os.path.join(folder_path, file))
        return files

    def show_image(self):
        if self.image_files and 0 <= self.current_image_index < len(self.image_files):
            image_path = self.image_files[self.current_image_index]
            try:
                img = Image.open(image_path)
                # Resize image to fit window if it's too large
                max_width = self.root.winfo_width() - 20
                max_height = self.root.winfo_height() - 100
                img.thumbnail((max_width, max_height))

                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo)
                self.image_label.image = photo # Keep a reference
                self.filename_label.config(text=os.path.basename(image_path))
            except Exception as e:
                messagebox.showerror("Error",f"Failed to open image {os.path.basename(image_path)}{e}")
                self.image_files.pop(self.current_image_index)
                if self.current_image_index >= len(self.image_files):
                    self.current_image_index -= 1
                self.show_image()


    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()
        self.update_button_states()

    def show_next_image(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.show_image()
        self.update_button_states()

    def update_button_states(self):
        if self.current_image_index <= 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        if self.current_image_index >= len(self.image_files) - 1:
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = ImageViewerApp(root)
    root.mainloop()
