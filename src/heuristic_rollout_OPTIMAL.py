import random


def heuristic_rollout(game, state):
    """Priority:
    1. WIN NOW
    2. BLOCK WIN NOW OF OPPONENT           
    3. CREATING 2-HEAD-OPENED (WIN_LENGTH-1) SEQUENCE                 
    4. BLOCK OPPONENT DOING(3) --> BLOCK 2-HEAD-OPENED-(LENGTH = 3) SEQUENCE
    5. RANDOM CHOICE IN "FRONTIER" 
    """

    #EDGE CASE
    winner = game.get_winner(state)
    if winner is not None:
        return winner


    size, win_len = game.size, game.win_length
    directions = game.DIRECTIONS
    board = [list(row) for row in state[0]]
    player = state[1]

    frontier = [] # BLANKS NEAR STONS
    f_index = {}  # INDEX OF FRONTIER (OPTIMIZATION FOR GETTING)
    win_cells = {1: set(), -1: set()} # Following cell in win_cells --> Simutaneous WIN
    threat_cells = {1: set(), -1: set()} # Threat alerting (when opponent is about to have 2-HEAD-OPENED - (LENGTH = 4) SEQUENCE) ~ Detecting 2-HEAD-OPENED-(LENGTH = 3) SEQUENCE


    def add_frontier(row, col):
        for near_r in range(max(0, row - 1), min(size, row + 2)):
            for near_c in range(max(0, col - 1), min(size, col + 2)):
                if board[near_r][near_c] == 0:
                    cell = (near_r, near_c)
                    if cell not in f_index:
                        f_index[cell] = len(frontier)
                        frontier.append(cell)

    def remove_frontier(cell):
        index = f_index.pop(cell, None)
        if index is not None:
            last_cell = frontier.pop()
            if last_cell != cell:
                frontier[index] = last_cell
                f_index[last_cell] = index

    def is_opened_threat(row, col, player):
        for diff_r, diff_c in directions:
            count = 1

            #THUAN
            near_r, near_c = row + diff_r , col + diff_c
            while 0 <= near_r < size and 0 <= near_c < size and board[near_r][near_c] == player:
                count += 1
                near_r += diff_r
                near_c += diff_c

            open1 = (0 <= near_r < size and 0 <= near_c < size and board[near_r][near_c] == 0)

            #NGUOC
            near_r, near_c = row - diff_r , col - diff_c
            while 0 <= near_r < size and 0 <= near_c < size and board[near_r][near_c] == player:
                count += 1
                near_r -= diff_r
                near_c -= diff_c

            open2 = (0 <= near_r < size and 0 <= near_c < size and board[near_r][near_c] == 0)

            if count == win_len - 1 and open1 and open2:
                return True
        return False

    def update_cells(row, col, player):
        """update win_cells + threat_cells after player does (row,col)"""
        for diff_r , diff_c in directions:
            count_1 = 0 
            near_r_1 , near_c_1 = row + diff_r , col + diff_c
            while 0 <= near_r_1 < size and 0 <= near_c_1 < size and board[near_r_1][near_c_1] == player:
                count_1 +=1 
                near_r_1 += diff_r 
                near_c_1 += diff_c


            count_2 = 0
            near_r_2, near_c_2 = row - diff_r, col - diff_c
            while 0 <= near_r_2 < size and 0 <= near_c_2 < size and board[near_r_2][near_c_2] == player:
                count_2 +=1
                near_r_2 -= diff_r
                near_c_2 -= diff_c

            mid_sequence = 1 + count_1 + count_2 # Total : LEFT sequence Player + PLAYER (Just taken) + RIGHT sequence Player
            #Right Open
            open1 = (0 <= near_r_1 < size and 0 <= near_c_1 < size and board[near_r_1][near_c_1] == 0)
            #Left Open
            open2 = (0 <= near_r_2 < size and 0 <= near_c_2 < size and board[near_r_2][near_c_2] == 0)

            if open1:
                extra_1 = 0
                new_r_1, new_c_1 = near_r_1 + diff_r, near_c_1 + diff_c
                while 0 <= new_r_1 < size and 0 <= new_c_1 < size and board[new_r_1][new_c_1] == player:
                    extra_1 += 1
                    new_r_1 += diff_r
                    new_c_1 += diff_c
                total_1 = mid_sequence + 1 + extra_1    # +1 : Blank pixel

                if total_1 >= win_len:
                    win_cells[player].add((near_r_1, near_c_1))
                elif total_1 == win_len - 1 and open2 and (0 <= new_r_1 < size and 0 <= new_c_1 < size and board[new_r_1][new_c_1] == 0):
                    threat_cells[player].add((near_r_1, near_c_1))

            if open2:
                extra_2 = 0
                new_r_2, new_c_2 = near_r_2 - diff_r, near_c_2 - diff_c
                while 0 <= new_r_2 < size and 0 <= new_c_2 < size and board[new_r_2][new_c_2] == player:
                    extra_2 += 1
                    new_r_2 -= diff_r
                    new_c_2 -= diff_c
                total_2 = mid_sequence + 1 + extra_2    # +1 : Blank pixel

                if total_2 >= win_len:
                    win_cells[player].add((near_r_2, near_c_2))
                elif total_2 == win_len - 1 and open1 and (0 <= new_r_2 < size and 0 <= new_c_2 < size and board[new_r_2][new_c_2] == 0):
                    threat_cells[player].add((near_r_2, near_c_2))

    def pop_valid(cell_set):
        while cell_set:
            cell = cell_set.pop()
            if board[cell[0]][cell[1]] == 0:
                return cell
        return None

    def pop_valid_threat(cell_set, player):
        while cell_set:
            row, col = cell_set.pop()
            if board[row][col] == 0 and is_opened_threat(row, col, player):
                return (row, col)
        return None

    has_stone = False
    for r in range(size):
        for c in range(size):
            if board[r][c] != 0:
                has_stone = True
                add_frontier(r, c)
                update_cells(r, c, board[r][c])

    if not has_stone:
        mid = size // 2
        board[mid][mid] = player
        add_frontier(mid, mid)
        player = -player

    while frontier:
        # Prior_1
        if pop_valid(win_cells[player]) is not None:
            return player

        move = (
            #Prior_2 : Block OPPONENT DOING WIN-NOW
            pop_valid(win_cells[-player])
            # RAISING THREAT TO OPPONENT
            or pop_valid_threat(threat_cells[player], player)
            # BLOCKING OPPONENT RAISING THREAT
            or pop_valid_threat(threat_cells[-player], -player)
        )
        if move is None:
            move = frontier[random.randrange(len(frontier))]

        remove_frontier(move)
        row, col = move
        board[row][col] = player
        add_frontier(row, col)
        update_cells(row, col, player)
        player = -player

    return None