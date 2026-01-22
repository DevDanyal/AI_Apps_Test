import tkinter as tk
import random

class ChatGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Chat")
        
        self.chat_history = tk.Text(self.master, state='disabled', width=50, height=20, wrap='word')
        self.chat_history.pack(pady=10)
        
        self.message_entry = tk.Entry(self.master, width=40)
        self.message_entry.pack(pady=10)
        
        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack()
        
        self.add_message("Bot: Hello! How can I help you today?")

    def send_message(self):
        user_message = self.message_entry.get()
        if user_message:
            self.add_message(f"You: {user_message}")
            self.message_entry.delete(0, 'end')
            self.bot_reply(user_message)
            
    def bot_reply(self, user_message):
        bot_responses = [
            "I'm not sure I understand. Can you rephrase that?",
            "That's interesting! Tell me more.",
            "I'm just a simple bot, I don't have all the answers.",
            "Let me think about that for a moment...",
            "I see. What else is on your mind?"
        ]
        
        bot_message = random.choice(bot_responses)
        self.add_message(f"Bot: {bot_message}")

    def add_message(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert('end', message + '\n')
        self.chat_history.config(state='disabled')
        self.chat_history.see('end')

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()
