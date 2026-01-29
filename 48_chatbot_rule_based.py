import tkinter as tk
from tkinter import scrolledtext, messagebox
import random

class RuleBasedChatbot:
    def __init__(self, master):
        self.master = master
        master.title("Rule-Based Chatbot")
        master.geometry("500x600")
        master.resizable(False, False)

        self.rules = self.load_rules()
        self.create_widgets()

    def load_rules(self):
        # Define some simple rules for the chatbot
        # Each rule is a tuple: (list of keywords, list of possible responses)
        return {
            "hello": ["Hi there!", "Hello!", "Greetings!"],
            "how are you": ["I'm a bot, so I don't have feelings, but I'm functioning well!", "I'm doing great, thanks for asking!"],
            "what is your name": ["I don't have a name.", "You can call me Chatbot.", "I am a simple rule-based chatbot."],
            "bye": ["Goodbye!", "See you later!", "Bye for now!"],
            "help": ["I can respond to simple greetings and questions.", "Try asking 'hello' or 'how are you'"],
            "thanks": ["You're welcome!", "No problem!", "Glad to help!"],
            "default": ["I'm not sure how to respond to that.", "Can you rephrase that?", "Interesting, tell me more.", "I'm still learning!"]
        }

    def create_widgets(self):
        # Conversation display area
        self.conversation_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled', width=60, height=25)
        self.conversation_display.pack(pady=10)

        # Input frame
        input_frame = tk.Frame(self.master)
        input_frame.pack(pady=10)

        self.user_input = tk.Entry(input_frame, width=45)
        self.user_input.pack(side=tk.LEFT, padx=5)
        self.user_input.bind("<Return>", self.send_message_event)

        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.display_message("Chatbot", "Hello! How can I help you today?")

    def display_message(self, sender, message):
        self.conversation_display.config(state='normal')
        self.conversation_display.insert(tk.END, f"{sender}: {message}\n")
        self.conversation_display.config(state='disabled')
        self.conversation_display.yview(tk.END) # Auto-scroll to the bottom

    def send_message_event(self, event):
        self.send_message()

    def send_message(self):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.display_message("You", user_text)
        self.user_input.delete(0, tk.END)

        self.get_bot_response(user_text)

    def get_bot_response(self, user_text):
        user_text_lower = user_text.lower()
        response = random.choice(self.rules["default"])

        for keyword, responses in self.rules.items():
            if keyword in user_text_lower and keyword != "default":
                response = random.choice(responses)
                break
        
        self.master.after(500, lambda: self.display_message("Chatbot", response)) # Simulate bot "thinking"

if __name__ == "__main__":
    root = tk.Tk()
    app = RuleBasedChatbot(root)
    root.mainloop()
