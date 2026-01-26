import tkinter as tk
from tkinter import messagebox

class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar Cipher Encryptor/Decryptor")
        self.root.geometry("500x450")

        # --- Input Frame ---
        self.input_frame = tk.LabelFrame(root, text="Input Text")
        self.input_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.input_text_widget = tk.Text(self.input_frame, height=8, width=50)
        self.input_text_widget.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        # --- Shift Key Frame ---
        self.key_frame = tk.Frame(root)
        self.key_frame.pack(pady=5, padx=10, fill=tk.X)

        self.key_label = tk.Label(self.key_frame, text="Shift Key (1-25):")
        self.key_label.pack(side=tk.LEFT, padx=5)
        self.key_entry = tk.Entry(self.key_frame, width=5)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        self.key_entry.insert(0, "3") # Default shift key

        # --- Buttons Frame ---
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10, padx=10, fill=tk.X)

        self.encrypt_button = tk.Button(self.button_frame, text="Encrypt", command=self.encrypt_text)
        self.encrypt_button.pack(side=tk.LEFT, padx=10, expand=True)

        self.decrypt_button = tk.Button(self.button_frame, text="Decrypt", command=self.decrypt_text)
        self.decrypt_button.pack(side=tk.RIGHT, padx=10, expand=True)

        # --- Output Frame ---
        self.output_frame = tk.LabelFrame(root, text="Output Text")
        self.output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.output_text_widget = tk.Text(self.output_frame, height=8, width=50, state="disabled")
        self.output_text_widget.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

    def caesar_cipher(self, text, shift, mode):
        result = ""
        for char in text:
            if 'a' <= char <= 'z':
                start = ord('a')
            elif 'A' <= char <= 'Z':
                start = ord('A')
            else:
                result += char
                continue

            if mode == "encrypt":
                shifted_char = chr(((ord(char) - start + shift) % 26) + start)
            elif mode == "decrypt":
                shifted_char = chr(((ord(char) - start - shift + 26) % 26) + start)
            result += shifted_char
        return result

    def encrypt_text(self):
        self.process_text("encrypt")

    def decrypt_text(self):
        self.process_text("decrypt")

    def process_text(self, mode):
        input_text = self.input_text_widget.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Input Error", "Please enter text to process.")
            return

        try:
            shift_key = int(self.key_entry.get())
            if not (1 <= shift_key <= 25):
                messagebox.showerror("Invalid Key", "Shift key must be an integer between 1 and 25.")
                return
        except ValueError:
            messagebox.showerror("Invalid Key", "Shift key must be an integer.")
            return

        processed_text = self.caesar_cipher(input_text, shift_key, mode)
        self.output_text_widget.config(state="normal")
        self.output_text_widget.delete("1.0", tk.END)
        self.output_text_widget.insert("1.0", processed_text)
        self.output_text_widget.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherApp(root)
    root.mainloop()
