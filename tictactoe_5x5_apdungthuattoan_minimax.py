"""
Tic Tac Toe Player
"""

import copy
import math
import random
import numpy

X = "X"
O = "O"
EMPTY = None
ai = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xCounter = 0
    oCounter = 0

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == X:
                xCounter += 1
            elif board[i][j] == O:
                oCounter += 1

    if xCounter > oCounter:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleActions = set()

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))
    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Create new board, without modifying the original board received as input
    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result

def get_horizontal_winner(board):
    winner_val = None
    board_len = len(board)
    for i in range(board_len):
        for k in range(3):
            winner_val = board[i][k]
            for j in range(board_len - 2):
                if board[i][k+j] != winner_val:
                    winner_val = None
            if winner_val:
                return winner_val
    return winner_val

def get_vertical_winner(board):
    winner_val = None
    board_len = len(board)
    for i in range(board_len):
        for k in range(3):
            winner_val = board[k][i]
            for j in range(board_len - 2):
                if board[j+k][i] != winner_val:
                    winner_val = None
            if winner_val:
                return winner_val
    return winner_val

#duong cheo chinh
def get_diagonal_mainbottom_winner(board):
    winner_val = None
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        winner_val = board[0][0]
    if board[1][1] == board[2][2] and board[2][2] == board[3][3]:
        winner_val = board[1][1]
    if board[2][2] == board[3][3] and board[3][3] == board[4][4]:
        winner_val = board[2][2]

    if board[1][0] == board[2][1] and board[2][1] == board[3][2]:
        winner_val = board[1][0]
    if board[2][1] == board[3][2] and board[3][2] == board[4][3]:
        winner_val = board[2][1]

    if board[2][0] == board[3][1] and board[3][1] == board[4][2]:
        winner_val = board[2][0]        
    return winner_val

def get_diagonal_maintop_winner(board):
    winner_val = None
    if board[0][1] == board[1][2] and board[1][2] == board[2][3]:
        winner_val = board[0][1]
    if board[1][2] == board[2][3] and board[2][3] == board[3][4]:
        winner_val = board[1][2]

    if board[0][2] == board[1][3] and board[1][3] == board[2][4]:
        winner_val = board[0][2]        
    return winner_val

#duong cheo phu
def get_diagonal_secbottom_winner(board):
    winner_val = None
    if board[0][4] == board[1][3] and board[1][3] == board[2][2]:
        winner_val = board[0][4]
    if board[1][3] == board[2][2] and board[2][2] == board[3][1]:
        winner_val = board[1][3]
    if board[2][2] == board[3][1] and board[3][1] == board[4][0]:
        winner_val = board[2][2]

    if board[1][4] == board[2][3] and board[2][3] == board[3][2]:
        winner_val = board[1][4]
    if board[2][3] == board[3][2] and board[3][2] == board[4][1]:
        winner_val = board[2][3]

    if board[2][4] == board[3][3] and board[3][3] == board[4][2]:
        winner_val = board[2][4]        
    return winner_val

def get_diagonal_sectop_winner(board):
    winner_val = None
    if board[0][3] == board[1][2] and board[1][2] == board[2][1]:
        winner_val = board[0][3]
    if board[1][2] == board[2][1] and board[2][1] == board[3][0]:
        winner_val = board[1][2]

    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        winner_val = board[0][2]        
    return winner_val


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner_val = get_horizontal_winner(board) or get_vertical_winner(board) or get_diagonal_mainbottom_winner(board) or get_diagonal_maintop_winner(board) or get_diagonal_secbottom_winner(board) or get_diagonal_sectop_winner(board)
    return winner_val

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
    return 0


def minimax(board, depth):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_value(board, depth)
            return move
        else:
            value, move = min_value(board, depth)
            return move


def max_value(board, depth):
    if terminal(board) or depth == 0:
        return utility(board), None

    v = -math.inf
    move = None
    for action in actions(board):
        # v = max(v, min_value(result(board, action)))
        aux, act = min_value(result(board, action), depth - 1)
        if aux > v:
            v = aux
            move = action
            if v == 1:
                return v, move

    return v, move


def min_value(board, depth):
    if terminal(board) or depth == 0:
        return utility(board), None

    v = math.inf
    move = None
    for action in actions(board):
        # v = max(v, min_value(result(board, action)))
        aux, act = max_value(result(board, action), depth - 1)
        if aux < v:
            v = aux
            move = action
            if v == -1:
                return v, move
    return v, move

if __name__ == "__main__":
    board = initial_state()
    ai_turn = False
    print("Choose a player")
    user = input()
    if user == "X":
        ai = "O"
    else:
        ai = "X"
    while True:
        game_over = terminal(board)
        playr = player(board)
        if game_over:
            winner = winner(board)
            if winner is None:
                print("Game Over: Tie.")
            else:
                print(f"Game Over: {winner} wins.")
            break;
        else:
            if user != playr and not game_over:
                if ai_turn:
                    print("Defeat him!!:")
                    move = minimax(board, 3)
                    board = result(board, move)
                    ai_turn = False
                    print(numpy.array(board))
                    print("-------------------------------")
                else:
                    ai_turn = True
            elif user == playr and not game_over:
                ai_turn = True
                print("Enter the position to move (row,col)")
                i = int(input("Row:"))
                j = int(input("Col:"))
                if board[i][j] == EMPTY:
                    board = result(board, (i, j))
                    print("Your turn:")
                    print(numpy.array(board))


    
