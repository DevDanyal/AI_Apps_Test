import tkinter as tk

class NewCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Another Calculator")
        master.geometry("300x400")
        master.resizable(False, False)

        self.expression = ""
        self.equation = tk.StringVar()

        # Use a Label for the display to prevent user typing
        self.display = tk.Label(master, textvariable=self.equation, font=('arial', 20, 'bold'), anchor='e', bg='white', padx=10)
        self.display.grid(row=0, column=0, columnspan=4, sticky='nsew', ipady=10)

        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('C', 4, 3),
            ('=', 5, 0), ('⌫', 5, 2)
        ]

        for (text, row, col) in buttons:
            if text == '=':
                btn = tk.Button(master, text=text, command=self.calculate, height=2, width=5, font=('arial', 12, 'bold'), bg='lightblue')
                btn.grid(row=row, column=col, columnspan=2, sticky='nsew', padx=5, pady=5)
            elif text == 'C':
                btn = tk.Button(master, text=text, command=self.clear, height=2, width=5, font=('arial', 12, 'bold'), bg='orange')
                btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
            elif text == '⌫':
                btn = tk.Button(master, text=text, command=self.backspace, height=2, width=5, font=('arial', 12, 'bold'))
                btn.grid(row=row, column=col, columnspan=2, sticky='nsew', padx=5, pady=5)
            else:
                # Use a lambda to capture the button text
                btn = tk.Button(master, text=text, command=lambda t=text: self.press(t), height=2, width=5, font=('arial', 12, 'bold'))
                btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
        
        # Configure grid weights to make buttons expand
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)
        for i in range(6):
            master.grid_rowconfigure(i, weight=1)


    def press(self, num):
        """Appends the pressed button's character to the expression."""
        self.expression += str(num)
        self.equation.set(self.expression)

    def calculate(self):
        """Calculates the expression."""
        try:
            if self.expression:
                total = str(eval(self.expression))
                self.equation.set(total)
                self.expression = total
        except (SyntaxError, ZeroDivisionError):
            self.equation.set("Error")
            self.expression = ""

    def clear(self):
        """Clears the expression and the display."""
        self.expression = ""
        self.equation.set("")

    def backspace(self):
        """Removes the last character from the expression."""
        if self.expression:
            self.expression = self.expression[:-1]
            self.equation.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = NewCalculator(root)
    root.mainloop()
