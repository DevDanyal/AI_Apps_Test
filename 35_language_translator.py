import tkinter as tk
from tkinter import ttk, messagebox

class LanguageTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Language Translator")
        self.root.geometry("600x400")

        self.languages = ["English", "Spanish", "French", "German"]
        # Basic mock translation dictionary
        self.translations = {
            ("English", "Spanish"): {
                "hello": "hola",
                "goodbye": "adiós",
                "thank you": "gracias",
                "please": "por favor",
                "yes": "sí",
                "no": "no",
                "how are you": "¿cómo estás?",
                "i love you": "te amo"
            },
            ("English", "French"): {
                "hello": "bonjour",
                "goodbye": "au revoir",
                "thank you": "merci",
                "please": "s'il vous plaît",
                "yes": "oui",
                "no": "non",
                "how are you": "comment allez-vous?",
                "i love you": "je t'aime"
            },
            ("English", "German"): {
                "hello": "hallo",
                "goodbye": "auf wiedersehen",
                "thank you": "danke",
                "please": "bitte",
                "yes": "ja",
                "no": "nein",
                "how are you": "wie geht es dir?",
                "i love you": "ich liebe dich"
            }
            # Add more languages and translations as needed, including reverse for now
        }
        # Add reverse translations for demonstration if not explicitly handled
        # This is a simplification; a proper system would handle language pairs symmetrically
        for (lang1, lang2), dict1 in list(self.translations.items()):
            if (lang2, lang1) not in self.translations:
                self.translations[(lang2, lang1)] = {v: k for k, v in dict1.items()}


        # --- UI Elements ---
        # Language Selection
        self.lang_frame = tk.Frame(root)
        self.lang_frame.pack(pady=10)

        self.from_lang_label = tk.Label(self.lang_frame, text="From:")
        self.from_lang_label.pack(side=tk.LEFT, padx=5)
        self.from_lang_combo = ttk.Combobox(self.lang_frame, values=self.languages, state="readonly")
        self.from_lang_combo.pack(side=tk.LEFT, padx=5)
        self.from_lang_combo.set("English")

        self.to_lang_label = tk.Label(self.lang_frame, text="To:")
        self.to_lang_label.pack(side=tk.LEFT, padx=5)
        self.to_lang_combo = ttk.Combobox(self.lang_frame, values=self.languages, state="readonly")
        self.to_lang_combo.pack(side=tk.LEFT, padx=5)
        self.to_lang_combo.set("Spanish")

        # Input Text
        self.input_label = tk.Label(root, text="Enter Text to Translate:")
        self.input_label.pack(pady=5)
        self.input_text_widget = tk.Text(root, height=5, width=60)
        self.input_text_widget.pack(pady=5)

        # Translate Button
        self.translate_button = tk.Button(root, text="Translate", command=self.translate_text)
        self.translate_button.pack(pady=10)

        # Output Text
        self.output_label = tk.Label(root, text="Translated Text:")
        self.output_label.pack(pady=5)
        self.output_text_widget = tk.Text(root, height=5, width=60, state="disabled")
        self.output_text_widget.pack(pady=5)

    def translate_text(self):
        from_lang = self.from_lang_combo.get()
        to_lang = self.to_lang_combo.get()
        input_text = self.input_text_widget.get("1.0", tk.END).strip().lower() # Convert to lower for dictionary lookup

        if not input_text:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return
        if not from_lang or not to_lang:
            messagebox.showerror("Selection Error", "Please select both source and target languages.")
            return
        if from_lang == to_lang:
            messagebox.showwarning("Same Language", "Source and target languages are the same.")
            self.output_text_widget.config(state="normal")
            self.output_text_widget.delete("1.0", tk.END)
            self.output_text_widget.insert("1.0", input_text)
            self.output_text_widget.config(state="disabled")
            return

        # Perform mock translation
        translated_text = self._mock_translate(input_text, from_lang, to_lang)

        self.output_text_widget.config(state="normal")
        self.output_text_widget.delete("1.0", tk.END)
        self.output_text_widget.insert("1.0", translated_text)
        self.output_text_widget.config(state="disabled")

    def _mock_translate(self, text, from_lang, to_lang):
        # A very basic, word-for-word mock translation
        words = text.split()
        translated_words = []
        
        # Determine the correct translation dictionary
        translation_dict = self.translations.get((from_lang, to_lang))
        if not translation_dict:
            # Try reversed lookup if not directly defined
            translation_dict = self.translations.get((to_lang, from_lang))
            if translation_dict:
                # If reversed, we need to reverse the lookup for each word
                reversed_dict = {v: k for k, v in translation_dict.items()}
                for word in words:
                    translated_words.append(reversed_dict.get(word, word)) # If not found, keep original word
                return " ".join(translated_words)
            else:
                return f"Translation not available from {from_lang} to {to_lang}. (Mock limitation)"


        for word in words:
            # Look up whole phrases first, then individual words
            found = False
            # Check for multi-word phrases (very basic, just checks if a multi-word key starts with current word)
            # This is a highly simplified approach for a mock; real translation is far more complex.
            for phrase, trans in translation_dict.items():
                if phrase.startswith(word) and len(phrase.split()) > 1:
                    # This logic would need to be much smarter to handle phrases correctly
                    # For a simple mock, we'll just check exact word matches
                    pass

            translated_words.append(translation_dict.get(word, word)) # If not found, keep original word
            
        # Add a note if translation was partial
        if any(w in input_text for w in words if w not in translation_dict):
            return " ".join(translated_words) + "\n(Some words not translated due to mock limitation)"
        else:
            return " ".join(translated_words)


if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageTranslatorApp(root)
    root.mainloop()
