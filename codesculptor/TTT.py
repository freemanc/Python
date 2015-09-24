"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 30         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 3.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    Perform a MC random trial
    """
    cur_player = player
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        next_tuple = random.choice(empty_squares)
        board.move(next_tuple[0], next_tuple[1], cur_player)
        cur_player = provided.switch_player(cur_player)
    else: 
        return
        
# Test for mc_trial
# board = provided.TTTBoard(3)
# mc_board = board.clone()
# mc_trial(mc_board, provided.PLAYERX)
# print mc_board

def mc_update_scores(scores, board, player):
    """
    Update scores based on the result of a trial
    """
    dim = board.get_dim()
    if board.check_win() == player:
        for row in range(dim):
            for col in range(dim):
                if board.square(row, col) == player:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] -= SCORE_OTHER
                    
    elif board.check_win() == provided.switch_player(player):
        for row in range(dim):
            for col in range(dim):
                if board.square(row, col) == player:
                    scores[row][col] -= SCORE_CURRENT
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] += SCORE_OTHER

# Test for mc_update_scores
# scores = [[0] * board.get_dim() for _ in range(board.get_dim())]
# print scores
# mc_update_scores(scores, mc_board, provided.PLAYERX)
# print scores

def get_best_move(board, scores):
    """
    Choose the highest scored square as the best move
    """
    empty_squares = board.get_empty_squares()
    max_score = None
    good_squares = []
    if empty_squares != []:
        for row_col in empty_squares:
            if max_score == None or scores[row_col[0]][row_col[1]] > max_score:
                good_squares = [row_col]
                max_score = scores[row_col[0]][row_col[1]]
            elif scores[row_col[0]][row_col[1]] == max_score:
                good_squares.append(row_col)
        return random.choice(good_squares)

# Test for get_best_move
# print get_best_move(board, scores)

def mc_move(board, player, trials):
    """
    Return the MC best move for current player represented as row, col
    """
    scores = [[0] * board.get_dim() for _ in range(board.get_dim())]
    for _ in range(trials):
        mc_board = board.clone()
        mc_trial(mc_board, player)
        mc_update_scores(scores, mc_board, player)
    
    return get_best_move(board, scores)

# Test for mc_move
# print mc_move(board, provided.PLAYERX, NTRIALS)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

