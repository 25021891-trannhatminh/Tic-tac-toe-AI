from game import Game
import random
def heuristic_rollout(state):
    winner  = Game.get_winner(state)
    if winner is not None:
        return winner 

    board = [list(row) for row in state[0]]
    player = state[1] # about to take action  
    empties = [ (row,column)
               for row in range(Game.size)
               for column in range(Game.size)
               if board[row][column] == 0]

    def fast_win(player):
        for row,col in empties:
            board[row][col] = player 
            can_win = Game.wins_at(board,row,col)
            board[row][col] = 0 # Undo 
            if can_win : 
                return (row,col)
        return None 

    while empties:
        move  = fast_win(player) or fast_win(-player) or  random.choice(empties)
        empties.remove(move)
        row , col = move 
        board[row][col] = player
        if Game.wins_at(board,row,col):
            return (row,col)
        player = -player 

    #IF NO WINNER 
    return None 