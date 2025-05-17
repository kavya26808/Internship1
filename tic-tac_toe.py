import tkinter as tk

#Backend logic

class TicTacToeGame:
    def __init__(self):
        self.board =[""] * 9
        self.current_player= "X"
        self.winner = None

    def make_move(self, index):
        if self.board[index] == "" and not self.winner:
            self.board[index] = self.current_player
            if self.check_winner():
                self.winner = self.current_player
            else:
                self.current_player = "O" if  self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for i, j, k in combos:
            if self.board[i] == self.board[j] == self.board[k] !="":
                return True
        return False

    def reset_game(self):
        self.__init__()

#frontend GUI using Tkinter

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Two Player Mode")

        #Fullscreen & styling
        self.root.attributes("-fullscreen",True)
        self.root.configure(bg="pink")

        self.game = TicTacToeGame()
        self.buttons = []

        #status label
        self.status_label = tk.Label(
            root, text="1st Player's Turn(X)",
            font=("Arial",24, "bold"), bg="pink", fg="black"
        )
        self.status_label.pack(pady=20)

        #game frame
        self.game_frame = tk.Frame(root, bg="black", bd=5)
        self.game_frame.pack()

        for i in range(9):
            btn = tk.Button(
                self.game_frame, text="", font=("Arial", 48, "bold"),
                width=5, height=2, bg="white", fg="black",
                command=lambda i=i: self.on_click(i)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)
        #reser & exit buttons
        self.control_frame = tk.Frame(root, bg="pink")
        self.control_frame.pack(pady=20)

        self.reset_button = tk.Button(
            self.control_frame, text="Exit", font=("Arial", 18),
            command=self.root.quit, bg="black", fg="white", width=10
      )
        

    def on_click(self, index):
        if self.game.make_move(index):
            self.update_board()
            if self.game.winner:
                winner = "1st player" if self.game.winner =="X" else "2nd player"
                self.status_label.config(text=f"{winner} ({self.game.winner}) wins!")
            elif "" not in self.game.board:
                self.status_label.config(text="It's a tie!")
            else:
                player = "1st player" if self.game.current_player == "X" else "2nd player"
                self.status_label.config(text=f"{player}'s Turn ({self.game.current_player})")
    def update_board(self):
        for i in range(9):
            self.buttons[i].config(text=self.game.board[i])
    def reset_game(self):
        self.game.reset_game()
        for btn in self.buttons:
            btn.config(text="")
        self.status-label.config(text="1st player's Turn (X)")


if __name__ == "__main__" :
    root=tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
