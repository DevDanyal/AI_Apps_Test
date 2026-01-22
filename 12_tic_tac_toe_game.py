import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text=' ', font=('normal', 40), width=5, height=2,
                                               command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)
        
        self.game_mode_var = tk.StringVar(value="2")
        
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        
        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.reset_game)
        game_menu.add_separator()
        
        game_mode_menu = tk.Menu(game_menu, tearoff=0)
        game_menu.add_cascade(label="Game Mode", menu=game_mode_menu)
        game_mode_menu.add_radiobutton(label="Two Players", variable=self.game_mode_var, value="1", command=self.reset_game)
        game_mode_menu.add_radiobutton(label="Player vs Computer", variable=self.game_mode_var, value="2", command=self.reset_game)

    def on_button_click(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            
            if self.check_winner(self.current_player):
                messagebox.showinfo("Tic Tac Toe", f"Player {self.current_player} wins!")
                self.reset_game()
            elif all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.game_mode_var.get() == "2" and self.current_player == 'O':
                    self.computer_move()
                    
    def computer_move(self):
        while True:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.board[row][col] == ' ':
                self.on_button_click(row, col)
                break

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def reset_game(self):
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=' ')

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
