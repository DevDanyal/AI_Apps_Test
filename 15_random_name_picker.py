import tkinter as tk
from tkinter import messagebox
import random

class RandomNamePickerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Random Name Picker")
        
        self.master.geometry("400x400")
        
        self.title_label = tk.Label(self.master, text="Enter names (one per line):", font=("normal", 14))
        self.title_label.pack(pady=10)
        
        self.name_text = tk.Text(self.master, height=10, width=30)
        self.name_text.pack(pady=10)
        
        self.pick_button = tk.Button(self.master, text="Pick a Random Name", command=self.pick_random_name)
        self.pick_button.pack(pady=20)
        
        self.result_label = tk.Label(self.master, text="", font=("normal", 16, "bold"))
        self.result_label.pack()

    def pick_random_name(self):
        names_input = self.name_text.get("1.0", "end-1c")
        names = [name.strip() for name in names_input.split("\n") if name.strip()]
        
        if not names:
            messagebox.showwarning("No Names", "Please enter at least one name.")
            return
            
        random_name = random.choice(names)
        self.result_label.config(text=f"The winner is:\n{random_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomNamePickerGUI(root)
    root.mainloop()
