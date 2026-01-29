import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import json

class DictionaryApp:
    def __init__(self, master):
        self.master = master
        master.title("Dictionary App")
        master.geometry("600x500")
        master.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Frame for input and search button
        input_frame = tk.Frame(self.master)
        input_frame.pack(pady=10)

        self.word_label = tk.Label(input_frame, text="Enter Word:")
        self.word_label.pack(side=tk.LEFT, padx=5)

        self.word_entry = tk.Entry(input_frame, width=30)
        self.word_entry.pack(side=tk.LEFT, padx=5)
        self.word_entry.bind("<Return>", self.search_word_event) # Bind Enter key

        self.search_button = tk.Button(input_frame, text="Search", command=self.search_word)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Scrolled text for displaying results
        self.result_text = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=70, height=20)
        self.result_text.pack(pady=10)
        self.result_text.config(state=tk.DISABLED) # Make it read-only

    def search_word_event(self, event):
        self.search_word()

    def search_word(self):
        word = self.word_entry.get().strip()
        if not word:
            messagebox.showwarning("Input Error", "Please enter a word to search.")
            return

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Searching for '{word}'...\n")
        self.result_text.config(state=tk.DISABLED) # Make it read-only

        # Placeholder for API call and result display
        self.fetch_definition(word)

    def fetch_definition(self, word):
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()

            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)

            if isinstance(data, list):
                for entry in data:
                    self.result_text.insert(tk.END, f"Word: {entry.get('word', 'N/A')}\n", "header")

                    phonetics = entry.get('phonetics', [])
                    if phonetics:
                        for phonetic in phonetics:
                            text = phonetic.get('text')
                            audio = phonetic.get('audio')
                            if text:
                                self.result_text.insert(tk.END, f"  Phonetic: {text}\n", "sub_header")
                            if audio:
                                self.result_text.insert(tk.END, f"  Audio: {audio}\n", "link")
                    else:
                        self.result_text.insert(tk.END, "  Phonetics: N/A\n", "sub_header")

                    meanings = entry.get('meanings', [])
                    for meaning in meanings:
                        part_of_speech = meaning.get('partOfSpeech', 'N/A')
                        self.result_text.insert(tk.END, f"\n  Part of Speech: {part_of_speech}\n", "sub_header")
                        definitions = meaning.get('definitions', [])
                        for i, definition in enumerate(definitions):
                            self.result_text.insert(tk.END, f"    {i+1}. {definition.get('definition', 'N/A')}\n", "normal")
                            example = definition.get('example')
                            if example:
                                self.result_text.insert(tk.END, f"       Example: \"{example}\"\n", "example")
                    self.result_text.insert(tk.END, "\n" + "="*50 + "\n\n", "separator")
            else: # Handle cases where API returns an error message as a dict
                self.result_text.insert(tk.END, f"Error: {data.get('title', 'Unknown Error')}\n", "error")
                self.result_text.insert(tk.END, f"Message: {data.get('message', 'No definition found.')}\n", "error")
                self.result_text.insert(tk.END, f"Resolution: {data.get('resolution', '')}\n", "error")

            self.result_text.tag_config("header", foreground="blue", font=("Helvetica", 14, "bold"))
            self.result_text.tag_config("sub_header", foreground="darkgreen", font=("Helvetica", 12, "bold"))
            self.result_text.tag_config("normal", font=("Helvetica", 10))
            self.result_text.tag_config("example", foreground="gray", font=("Helvetica", 10, "italic"))
            self.result_text.tag_config("link", foreground="purple", font=("Helvetica", 10, "underline"))
            self.result_text.tag_config("error", foreground="red", font=("Helvetica", 12, "bold"))
            self.result_text.tag_config("separator", foreground="orange")


        except requests.exceptions.HTTPError as http_err:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            if response.status_code == 404:
                self.result_text.insert(tk.END, f"Error: Word '{word}' not found.\n", "error")
            else:
                self.result_text.insert(tk.END, f"HTTP error occurred: {http_err}\n", "error")
            self.result_text.tag_config("error", foreground="red", font=("Helvetica", 12, "bold"))
        except requests.exceptions.ConnectionError as conn_err:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Connection Error: Please check your internet connection. {conn_err}\n", "error")
            self.result_text.tag_config("error", foreground="red", font=("Helvetica", 12, "bold"))
        except requests.exceptions.Timeout as timeout_err:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Timeout Error: The request timed out. {timeout_err}\n", "error")
            self.result_text.tag_config("error", foreground="red", font=("Helvetica", 12, "bold"))
        except requests.exceptions.RequestException as req_err:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"An unexpected error occurred: {req_err}\n", "error")
            self.result_text.tag_config("error", foreground="red", font=("Helvetica", 12, "bold"))
        finally:
            self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()
