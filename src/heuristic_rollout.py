import random
def heuristic_rollout(game,state):
    winner  = game.get_winner(state)
    if winner is not None:
        return winner 

    board = [list(row) for row in state[0]]
    player = state[1] # about to take action  

    empties  = []
    frontier = set()
    count = {1:0, -1:0}

    for row in range(game.size):
        for col in range(game.size):
            value = board[row][col]
            if value ==0:
                empties.append((row,col))
            else:
                count[value] += 1
                for near_row in range(max(0,row-1),min(game.size,row+2)):
                    for near_col in range(max(0,row-1),min(game.size,row+2)):
                        if board[near_row][near_col] ==0 :
                            frontier.add((near_row,near_col))


    def fast_win(player):
        if count[player] < game.win_length -1:
            return None
        
        for row,col in empties:
            board[row][col] = player 
            can_win = game.wins_at(board,row,col)
            board[row][col] = 0 # Undo 
            if can_win : 
                return (row,col)
        return None 

    while empties:
        # Fast Win --> Block (Fast Win Of Opponent) --> Random Choice\
        if fast_win(player) is not None: 
            return player
        move  = fast_win(-player) or  random.choice(empties)
        empties.remove(move)
        frontier.discard(move)

        row , col = move 
        board[row][col] = player
        count[player] +=1 

        for near_row in range(max(0,row-1),min(game.size,row+2)):
            for near_col in range(max(0,row-1),min(game.size,row+2)):
                if board[near_row][near_col] ==0 :
                    frontier.add((near_row,near_col))
        player = -player
    #IF NO WINNER 
    return None 