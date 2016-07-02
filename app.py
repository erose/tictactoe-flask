from flask import Flask
from flask import request, abort
import re
app = Flask(__name__)

def is_valid(board):
    """ Checks both whether the board is a valid representation of a tictacoe board, and whether it could be o's turn. """
    return re.match(r'[o x]{9}', board) and (board.count("x") - board.count("o") in [0, 1])
def is_tie(board):
    return not (" " in board)
def is_winner(board, player):
    three_in_a_row = [player, player, player]
    horizontals = [
        [board[0], board[1], board[2]] == three_in_a_row,
        [board[3], board[4], board[5]] == three_in_a_row,
        [board[6], board[7], board[8]] == three_in_a_row
    ]
    verticals = [
        [board[0], board[3], board[6]] == three_in_a_row,
        [board[1], board[4], board[7]] == three_in_a_row,
        [board[2], board[5], board[8]] == three_in_a_row
    ]
    diagonals = [
        [board[0], board[4], board[8]] == three_in_a_row,
        [board[2], board[4], board[6]] == three_in_a_row
    ]
    return any(horizontals) or any(verticals) or any(diagonals)

def other_player(player):
    return {'o': 'x', 'x': 'o'}[player]
def move(board, index, player):
    splits = list(board)
    splits[index] = player
    return "".join(splits)
def candidate_boards(board, player):
    return [move(board, i, player) for i, char in enumerate(board) if char == " "]
def score(board, player):
    """ Returns -1 if player will lose on this board, 0 if player can tie, and 1 if player can win. """
    opp = other_player(player)
    if is_winner(board, player):
        return 1
    if is_winner(board, opp):
        return -1 
    if is_tie(board):
        return 0

    candidates = candidate_boards(board, player)
    return max(-1 * score(candidate, opp) for candidate in candidates)

@app.route('/')
def main():
    board = request.args.get('board', None)
    if board is None or not is_valid(board) or is_tie(board) or is_winner(board, 'x') or is_winner(board, 'o'):
       abort(400) 

    candidates = candidate_boards(board, 'o')
    return max(candidates, key=lambda candidate: -1 * score(candidate, 'x'))
    # return candidate_boards(board, player='o')[0]
