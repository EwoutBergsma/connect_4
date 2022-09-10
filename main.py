import numpy as np
from scipy import ndimage

# Parameters
board_height = 6  # Vertical board size
board_width = 7  # Horizontal board size
n_connect = 4  # E.g. changes connect 4 to a connect 3 game, if changed to 3

board = np.zeros(shape=(board_height, board_width))  # For remainder of code board will be considered upside-down
# board = np.where(board == 0, "_", board)  # Replacing zeros with underscores, for prettier printing
legal_user_inputs = [str(i) for i in range(board_width)]  # Computing legal user inputs (i.e. 0 to 6 in this case)


# Prints the board in a humanly readable manner
def print_board(board, empty_terminal=True):
    if empty_terminal:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")  # There may be a better way of flushing terminal (\n is a new line)
    board = np.flip(board, 0)  # In the background the board is flipped. For human reading we flip it before printing
    for row in board:  # This loops through all the rows of board, populating the row variable with the row content
        for element in row:
            print(int(element), " ", end="")  # end="" makes sure not to print a new line after the print
        print()

    print("___________________")
    # Following prints the column number underneath the board
    for input in legal_user_inputs:
        print(input, " ", end="")
    print()  # Just a new line


# Requests the user to input their next move, also tests if move is legal, returns new board state if legal
def ask_user_input(board, turn):
    print(f"Player {turn % 2 + 1}'s turn, ", end="")

    user_input = input("type column [0-6]: ")
    if user_input in legal_user_inputs:
        for row_index, element in enumerate(board[:, int(user_input):int(user_input) + 1]):
            if element == 0:
                board[row_index, int(user_input)] = turn % 2 + 1  # Note how user_input is the column index
                break  # This stops the for loop
            if row_index == len(board[:, int(user_input):int(user_input) + 1]) - 1:
                print("COLUMN FULL, TRY AGAIN")
                ask_user_input(board, turn)
    else:
        print("INCCORECT INPUT, TRY AGAIN")
        ask_user_input(board, turn)

    return board


# ONLY checks for horizontal wins for current player. Returns False for no win, True for win.
def _check_horizontal_win(board, turn):
    indices = np.array(range(n_connect))
    for row in board:  # This loops through all the rows of board, populating the row variable with the row content
        # a numpy array can be indexed by a numpy array in order to obtain a subset of the array
        for offset in range(len(board[0])-n_connect):  # To offset the above indices such that all horizontal winning combinations are checked
            connect_combination = row[indices + offset]
            if np.count_nonzero(connect_combination == turn % 2 + 1) == n_connect:
                return True
    return False


# Checks win horizontally, vertically and diagonally for current player. Returns True if won, False if not.
def check_win(board, turn):
    # Rotating board 0 degrees, 90 degrees and 45 degrees, then checking if current player has won.
    return _check_horizontal_win(board, turn) or _check_horizontal_win(np.rot90(board), turn) or _check_horizontal_win(np.array(ndimage.rotate(board, 45, reshape=True, order=0)), turn)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    turn = -1
    while not check_win(board, turn):
        turn += 1
        print_board(board)
        ask_user_input(board, turn)

    print_board(board)
    print(f"\nPlayer {turn % 2 + 1} won in turn {turn+1}!!")
