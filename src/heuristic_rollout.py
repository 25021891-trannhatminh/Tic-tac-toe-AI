import random
def heuristic_rollout(game,state):
    winner  = game.get_winner(state)
    if winner is not None:
        return winner 

    board = [list(row) for row in state[0]]
    player = state[1] # about to take action  

    empties = set() # full blanks of the board
    frontier = set() # only blanks near stone(current location of X and O)
    win_cells = {1:set(), -1 : set()} # Blanks that putting "X" ,"O" : win luon

    #Initiating empties and frontier
    for row in range(game.size):
        for col in range(game.size):
            value = board[row][col]
            if value ==0:
                empties.add((row,col))
            else:
                for near_row in range(max(0,row-1),min(game.size,row+2)):
                    for near_col in range(max(0,row-1),min(game.size,row+2)):
                        if board[near_row][near_col] ==0 :
                            frontier.add((near_row,near_col))

    #Find win_cells according to frontier
    for row,col in frontier:
        for player in (1,-1):
            board[row][col]= player
            if game.wins_at(board,row,col):
                win_cells[player].add((row,col))
            #Undo 
            board[row][col] = 0

    def update_win_cells(row,col,player):
        """
        After player putting p in (row,col), checking 8 blanks around p for updating win_cells

        """
        for diff_r, diff_c in game.DIRECTIONS: 
            near_r, near_c = row + diff_r , col + diff_c
            # T
            while 0 <= near_r < game.size and 0<= near_c < game.size and board[near_r][near_c] ==player:
                near_r += diff_r
                near_c += diff_c
            if 0 <= near_r < game.size and 0<= near_c < game.size and board[near_r][near_c] ==0 :
                board[near_r][near_c] = player
                if game.wins_at(board,near_r,near_c):
                    win_cells[player].add((near_r,near_c))
                board[near_r][near_c] =0
            # N
            while 0 <= near_r < game.size and 0<= near_c < game.size and board[near_r][near_c] ==player:
                near_r -= diff_r
                near_c -= diff_c
            if 0 <= near_r < game.size and 0<= near_c < game.size and board[near_r][near_c] ==0 :
                board[near_r][near_c] = player
                if game.wins_at(board,near_r,near_c):
                    win_cells[player].add((near_r,near_c))
                board[near_r][near_c] =0

    def pop_valid(cell_set):
        """Pick one blank in win_cells (skip stones)"""
        while cell_set:
            cell = cell_set.pop()
            if board[cell[0]][cell[1]] == 0:
                return cell
        return None

    while empties:
        # Win 
        if pop_valid(win_cells[player]) is not None:
            return player 

        #Block --> Random
        move = pop_valid(win_cells[-player])
        if move is None: 
            pool_action = tuple(frontier) if frontier else tuple(empties)
            move = random.choice(pool_action)

        empties.remove(move)
        frontier.discard(move)
        row , col = move 
        board[row][col] = player

        for near_row in range(max(0,row-1),min(game.size,row+2)):
            for near_col in range(max(0,row-1),min(game.size,row+2)):
                if board[near_row][near_col] ==0 :
                    frontier.add((near_row,near_col))
        update_win_cells(row,col,player)
        player = -player
    #IF NO WINNER 
    return None 