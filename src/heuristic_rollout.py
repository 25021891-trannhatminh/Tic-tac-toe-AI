import random
def heuristic_rollout(game,state):
    winner  = game.get_winner(state)
    if winner is not None:
        return winner 

    board = [list(row) for row in state[0]]
    player = state[1] # about to take action  
    empties = [ (row,column)
               for row in range(game.size)
               for column in range(game.size)
               if board[row][column] == 0]

    def fast_win(player):
        for row,col in empties:
            board[row][col] = player 
            can_win = game.wins_at(board,row,col)
            board[row][col] = 0 # Undo 
            if can_win : 
                return player 
        return None 

    while empties:
        # Fast Win --> Block (Fast Win Of Opponent) --> Random Choice
        move  = fast_win(player) or fast_win(-player) or  random.choice(empties)
        empties.remove(move)
        row , col = move 
        board[row][col] = player
        if game.wins_at(board,row,col):
            return player
        player = -player 

    #IF NO WINNER 
    return None 