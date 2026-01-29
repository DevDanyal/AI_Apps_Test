import tkinter as tk
from tkinter import messagebox, filedialog
import os
import random

class FlashcardApp:
    def __init__(self, master):
        self.master = master
        master.title("Flashcard Learning App")
        master.geometry("500x400")
        master.resizable(False, False)

        self.flashcards = []
        self.current_card_index = -1
        self.showing_answer = False

        self.create_widgets()
        self.load_flashcards_from_file() # Load default or last used file

    def create_widgets(self):
        # Question/Answer Display
        self.qa_frame = tk.Frame(self.master, bd=2, relief="groove", width=450, height=200)
        self.qa_frame.pack(pady=20)
        self.qa_frame.pack_propagate(False) # Prevent frame from resizing to label

        self.display_label = tk.Label(self.qa_frame, text="Load flashcards to begin", wraplength=400, justify=tk.CENTER, font=("Arial", 16))
        self.display_label.pack(expand=True)

        # Navigation Buttons
        nav_button_frame = tk.Frame(self.master)
        nav_button_frame.pack(pady=10)

        self.prev_button = tk.Button(nav_button_frame, text="Previous", command=self.show_prev_card, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.show_answer_button = tk.Button(nav_button_frame, text="Show Answer", command=self.toggle_qa, state=tk.DISABLED)
        self.show_answer_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(nav_button_frame, text="Next", command=self.show_next_card, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # File Operations
        file_button_frame = tk.Frame(self.master)
        file_button_frame.pack(pady=10)

        self.load_button = tk.Button(file_button_frame, text="Load Flashcards", command=self.load_flashcards_from_dialog)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.master, text="0/0 Flashcards", font=("Arial", 10))
        self.status_label.pack(pady=5)

    def load_flashcards_from_file(self, filepath="flashcards.txt"):
        if not os.path.exists(filepath):
            messagebox.showinfo("Info", "No default 'flashcards.txt' found. Please load a file.")
            self.flashcards = []
            self.current_card_index = -1
            self.update_card_display()
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.flashcards = []
                for i in range(0, len(lines) - 1, 2):
                    question = lines[i].strip()
                    answer = lines[i+1].strip()
                    if question and answer:
                        self.flashcards.append({"question": question, "answer": answer})
            
            if self.flashcards:
                self.current_card_index = 0
                self.update_card_display()
                self.enable_nav_buttons()
            else:
                messagebox.showinfo("Info", "Loaded file is empty or malformed.")
                self.current_card_index = -1
                self.disable_nav_buttons()

        except Exception as e:
            messagebox.showerror("Error", f"Could not load flashcards: {e}")
            self.current_card_index = -1
            self.flashcards = []
            self.disable_nav_buttons()
        self.update_status_label()

    def load_flashcards_from_dialog(self):
        filepath = filedialog.askopenfilename(
            title="Select Flashcard File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filepath:
            self.load_flashcards_from_file(filepath)

    def update_card_display(self):
        if not self.flashcards or self.current_card_index == -1:
            self.display_label.config(text="No flashcards loaded.")
            self.disable_nav_buttons()
            return

        card = self.flashcards[self.current_card_index]
        if self.showing_answer:
            self.display_label.config(text=card["answer"])
            self.show_answer_button.config(text="Hide Answer")
        else:
            self.display_label.config(text=card["question"])
            self.show_answer_button.config(text="Show Answer")
        self.update_status_label()

    def update_status_label(self):
        if self.flashcards:
            self.status_label.config(text=f"{self.current_card_index + 1}/{len(self.flashcards)} Flashcards")
        else:
            self.status_label.config(text="0/0 Flashcards")

    def show_next_card(self):
        self.showing_answer = False
        if self.flashcards:
            self.current_card_index = (self.current_card_index + 1) % len(self.flashcards)
            self.update_card_display()

    def show_prev_card(self):
        self.showing_answer = False
        if self.flashcards:
            self.current_card_index = (self.current_card_index - 1 + len(self.flashcards)) % len(self.flashcards)
            self.update_card_display()

    def toggle_qa(self):
        self.showing_answer = not self.showing_answer
        self.update_card_display()

    def enable_nav_buttons(self):
        self.prev_button.config(state=tk.NORMAL)
        self.show_answer_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)

    def disable_nav_buttons(self):
        self.prev_button.config(state=tk.DISABLED)
        self.show_answer_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
