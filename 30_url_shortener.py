import tkinter as tk
from tkinter import messagebox
import random
import string
import hashlib

class URLShortenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic URL Shortener")
        self.root.geometry("500x300")

        self.shortened_urls = {} # Stores {short_code: long_url}
        self.base_url = "http://short.url/"

        # --- UI Elements ---
        self.long_url_label = tk.Label(root, text="Enter Long URL:")
        self.long_url_label.pack(pady=10)

        self.long_url_entry = tk.Entry(root, width=60)
        self.long_url_entry.pack(pady=5)

        self.shorten_button = tk.Button(root, text="Shorten URL", command=self.shorten_url)
        self.shorten_button.pack(pady=10)

        self.short_url_label_prefix = tk.Label(root, text="Shortened URL:")
        self.short_url_label_prefix.pack(pady=5)
        
        self.short_url_text = tk.StringVar()
        self.short_url_display = tk.Entry(root, textvariable=self.short_url_text, width=40, state="readonly")
        self.short_url_display.pack(pady=5)

        self.copy_button = tk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard, state="disabled")
        self.copy_button.pack(pady=5)

        self.info_label = tk.Label(root, text="Note: This is a simulated local shortener. URLs are not publicly accessible.", fg="gray")
        self.info_label.pack(pady=10)

    def generate_short_code(self, long_url):
        # A simple hash-based approach for unique codes, or a random string
        # For a truly unique and collision-free system, a database would be needed.
        # Here, we'll use a portion of a hash to keep it somewhat consistent for the same input.
        hash_object = hashlib.md5(long_url.encode())
        hex_dig = hash_object.hexdigest()
        
        # Take a part of the hash and convert to base62 for shorter code
        # This is a simplification; collisions are possible but less likely with longer hashes.
        short_code_length = 6 # e.g., http://short.url/XXXXXX
        chars = string.ascii_letters + string.digits
        
        # Attempt to create a unique code by taking a slice of the hash
        # and re-hashing if necessary (though for this local demo, it's illustrative)
        potential_code = ''.join(random.choice(chars) for _ in range(short_code_length))
        
        # Ensure the generated code is unique for this session
        while potential_code in self.shortened_urls:
            potential_code = ''.join(random.choice(chars) for _ in range(short_code_length))
            
        return potential_code


    def shorten_url(self):
        long_url = self.long_url_entry.get().strip()

        if not long_url:
            messagebox.showwarning("Input Error", "Please enter a URL.")
            return

        if not (long_url.startswith("http://") or long_url.startswith("https://")):
            messagebox.showerror("Invalid URL", "URL must start with 'http://' or 'https://'.")
            return

        # Check if URL already shortened
        for short_code, stored_long_url in self.shortened_urls.items():
            if stored_long_url == long_url:
                short_url = self.base_url + short_code
                self.short_url_text.set(short_url)
                self.copy_button.config(state="normal")
                messagebox.showinfo("Already Shortened", f"This URL was already shortened to: {short_url}")
                return

        short_code = self.generate_short_code(long_url)
        self.shortened_urls[short_code] = long_url
        
        short_url = self.base_url + short_code
        self.short_url_text.set(short_url)
        self.copy_button.config(state="normal")
        messagebox.showinfo("URL Shortened", "URL shortened successfully!")

    def copy_to_clipboard(self):
        short_url = self.short_url_text.get()
        if short_url:
            self.root.clipboard_clear()
            self.root.clipboard_append(short_url)
            messagebox.showinfo("Copied", "Short URL copied to clipboard!")
        else:
            messagebox.showwarning("Copy Error", "No URL to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = URLShortenerApp(root)
    root.mainloop()
