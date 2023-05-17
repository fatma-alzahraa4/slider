import tkinter as tk
from tkinter import ttk
import numpy as np

# Define the game state
board_rows = 6
board_cols = 7
board = np.zeros((board_rows, board_cols))

# Define the game rules and AI algorithm
# ...

# Define the GUI
class GameGUI:
    def _init_(self, master):
        self.master = master
        master.title("Connect Four")

        self.algorithm = tk.StringVar(value="minimax")
        self.difficulty = tk.StringVar(value="medium")

        self.algorithm_label = ttk.Label(master, text="Select AI algorithm:")
        self.algorithm_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.algorithm_menu = ttk.OptionMenu(master, self.algorithm, "minimax", "minimax", "alpha-beta pruning")
        self.algorithm_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.difficulty_label = ttk.Label(master, text="Select difficulty level:")
        self.difficulty_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.difficulty_menu = ttk.OptionMenu(master, self.difficulty, "medium", "easy", "medium", "hard")
        self.difficulty_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.start_button = ttk.Button(master, text="Start game", command=self.start_game)
        self.start_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def start_game(self):
        # Get the selected algorithm and difficulty level
        algorithm = self.algorithm.get()
        difficulty = self.difficulty.get()

        # Start the game with the selected settings
        # ...
        print("Starting game with algorithm:", algorithm, "and difficulty:", difficulty)

# Start the GUI
root = tk.Tk()
game_gui = GameGUI(root)
root.mainloop()

def start_game(self):
    # Get the selected algorithm and difficulty level
    algorithm = self.algorithm.get()
    difficulty = self.difficulty.get()

    # Initialize the AI agent
    if algorithm == "minimax":
        if difficulty == "easy":
            depth = 5
        elif difficulty == "medium":
            depth = 7
        elif difficulty == "hard":
            depth = 10
        ai_agent = lambda board: minimax(board, depth, -np.Inf, np.Inf, True)[0]
    elif algorithm == "alpha-beta pruning":
        if difficulty == "easy":
            depth = 5
        elif difficulty == "medium":
            depth = 7
        elif difficulty == "hard":
            depth = 10
        ai_agent = lambda board: alphabeta(board, depth, -np.Inf, np.Inf, True)[0]

    # Start the game with the selected settings
    # ...
    print("Starting game with algorithm:", algorithm, "and difficulty:", difficulty)
    print("AI agent:", ai_agent)


# Define the game rules
def is_valid_location(board, col):
    return board[board_rows-1][col] == 0

def get_next_open_row(board, col):
    for r in range(board_rows):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(board_cols - 3):
        for r in range(board_rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(board_cols):
        for r in range(board_rows - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(board_cols - 3):
        for r in range(board_rows - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(board_cols - 3):
        for r in range(3, board_rows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = 1
    if piece == 1:
        opp_piece = 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, board_cols//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(board_rows):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(board_cols-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(board_cols):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(board_rows-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(board_rows-3):
        for c in range(board_cols-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(board_rows-3):
        for c in range(board_cols-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# Implement the Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = [col for col in range(board_cols) if is_valid_location(board, col)]

    # Check if game is over or maximum depth is reached
    if depth == 0 or len(valid_locations) == 0:
        if winning_move(board, 2):
            return (None, 100000000000000)
        elif winning_move(board, 1):
            return (None, -10000000000000)
        else:
            return (None, score_position(board, 2))

    if maximizing_player:
        value = -np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 1)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Play the game
game_over = False
turn = 0

while not game_over:
    # Player 1 input
    if turn == 0:
        col = int(input("Player 1 make your selection (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                print("PLAYER 1 WINS!")
                game_over = True

            turn += 1

    # Player 2 input (AI agent)
    if turn == 1 and not game_over:
        col, minimax_score = minimax(board, 5, -np.Inf, np.Inf, True)
        print("AI agent selects column:", col)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                print("AI AGENT WINS!")
                game_over = True

            turn -= 1

    print(board)

    if game_over:
        break


















import tkinter as tk
from tkinter import ttk
import numpy as np

# Define the game state
board_rows = 6
board_cols = 7
board = np.zeros((board_rows, board_cols))

# Define the game rules and AI algorithm
# ...

# Define the GUI
class GameGUI:
    def _init_(self, master):
        self.master = master
        master.title("Connect Four")

        self.algorithm = tk.StringVar(value="minimax")
        self.difficulty = tk.StringVar(value="medium")

        self.algorithm_label = ttk.Label(master, text="Select AI algorithm:")
        self.algorithm_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.algorithm_menu = ttk.OptionMenu(master, self.algorithm, "minimax", "minimax", "alpha-beta pruning")
        self.algorithm_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.difficulty_label = ttk.Label(master, text="Select difficulty level:")
        self.difficulty_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.difficulty_menu = ttk.OptionMenu(master, self.difficulty, "medium", "easy", "medium", "hard")
        self.difficulty_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.start_button = ttk.Button(master, text="Start game", command=self.start_game)
        self.start_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def start_game(self):
        # Get the selected algorithm and difficulty level
        algorithm = self.algorithm.get()
        difficulty = self.difficulty.get()

        # Start the game with the selected settings
        # ...
        print("Starting game with algorithm:", algorithm, "and difficulty:", difficulty)

# Start the GUI
root = tk.Tk()
game_gui = GameGUI(root)
root.mainloop()

def start_game(self):
    # Get the selected algorithm and difficulty level
    algorithm = self.algorithm.get()
    difficulty = self.difficulty.get()

    # Initialize the AI agent
    if algorithm == "minimax":
        if difficulty == "easy":
            depth = 5
        elif difficulty == "medium":
            depth = 7
        elif difficulty == "hard":
            depth = 10
        ai_agent = lambda board: minimax(board, depth, -np.Inf, np.Inf, True)[0]
    elif algorithm == "alpha-beta pruning":
        if difficulty == "easy":
            depth = 5
        elif difficulty == "medium":
            depth = 7
        elif difficulty == "hard":
            depth = 10
        ai_agent = lambda board: alphabeta(board, depth, -np.Inf, np.Inf, True)[0]

    # Start the game with the selected settings
    # ...
    print("Starting game with algorithm:", algorithm, "and difficulty:", difficulty)
    print("AI agent:", ai_agent)


# Define the game rules
def is_valid_location(board, col):
    return board[board_rows-1][col] == 0

def get_next_open_row(board, col):
    for r in range(board_rows):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(board_cols - 3):
        for r in range(board_rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(board_cols):
        for r in range(board_rows - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(board_cols - 3):
        for r in range(board_rows - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(board_cols - 3):
        for r in range(3, board_rows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = 1
    if piece == 1:
        opp_piece = 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, board_cols//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(board_rows):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(board_cols-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(board_cols):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(board_rows-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(board_rows-3):
        for c in range(board_cols-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(board_rows-3):
        for c in range(board_cols-3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# Implement the Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = [col for col in range(board_cols) if is_valid_location(board, col)]

    # Check if game is over or maximum depth is reached
    if depth == 0 or len(valid_locations) == 0:
        if winning_move(board, 2):
            return (None, 100000000000000)
        elif winning_move(board, 1):
            return (None, -10000000000000)
        else:
            return (None, score_position(board, 2))

    if maximizing_player:
        value = -np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 1)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Play the game
game_over = False
turn = 0

while not game_over:
    # Player 1 input
    if turn == 0:
        col = int(input("Player 1 make your selection (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                print("PLAYER 1 WINS!")
                game_over = True

            turn += 1

    # Player 2 input (AI agent)
    if turn == 1 and not game_over:
        col, minimax_score = minimax(board, 5, -np.Inf, np.Inf, True)
        print("AI agent selects column:", col)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                print("AI AGENT WINS!")
                game_over = True

            turn -= 1

    print(board)

    if game_over:
        break
