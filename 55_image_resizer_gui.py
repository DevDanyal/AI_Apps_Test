import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer Tool")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        self.image_path = tk.StringVar()
        self.new_width = tk.StringVar()
        self.new_height = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Frame for input fields
        input_frame = tk.LabelFrame(self.root, text="Image Details", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill="x")

        # Image Path
        tk.Label(input_frame, text="Image Path:").grid(row=0, column=0, sticky="w", pady=5)
        self.path_entry = tk.Entry(input_frame, textvariable=self.image_path, width=40)
        self.path_entry.grid(row=0, column=1, pady=5, padx=5)
        tk.Button(input_frame, text="Browse", command=self.browse_image).grid(row=0, column=2, pady=5, padx=5)

        # New Width
        tk.Label(input_frame, text="New Width:").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(input_frame, textvariable=self.new_width, width=15).grid(row=1, column=1, sticky="w", pady=5, padx=5)

        # New Height
        tk.Label(input_frame, text="New Height:").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(input_frame, textvariable=self.new_height, width=15).grid(row=2, column=1, sticky="w", pady=5, padx=5)

        # Resize Button
        resize_button = tk.Button(self.root, text="Resize Image", command=self.resize_image, padx=20, pady=10)
        resize_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack(pady=5)

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.ico")]
        )
        if file_path:
            self.image_path.set(file_path)
            self.status_label.config(text="")

    def resize_image(self):
        self.status_label.config(text="Processing...", fg="blue")
        image_file = self.image_path.get()
        width_str = self.new_width.get()
        height_str = self.new_height.get()

        if not image_file:
            self.status_label.config(text="Error: Please select an image file.", fg="red")
            return

        if not width_str or not height_str:
            self.status_label.config(text="Error: Please enter both width and height.", fg="red")
            return

        try:
            width = int(width_str)
            height = int(height_str)
            if width <= 0 or height <= 0:
                raise ValueError("Width and height must be positive integers.")
        except ValueError as e:
            self.status_label.config(text=f"Error: Invalid dimensions. {e}", fg="red")
            return

        try:
            img = Image.open(image_file)
            resized_img = img.resize((width, height), Image.LANCZOS)

            # Construct new filename
            base, ext = os.path.splitext(image_file)
            new_file_path = f"{base}_resized{ext}"

            resized_img.save(new_file_path)
            self.status_label.config(text=f"Image resized and saved to:\n{new_file_path}", fg="green")
        except FileNotFoundError:
            self.status_label.config(text="Error: Image file not found.", fg="red")
        except Exception as e:
            self.status_label.config(text=f"An error occurred: {e}", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
