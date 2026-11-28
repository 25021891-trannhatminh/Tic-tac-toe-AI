import random 

class Game: 
    """
    *General Tic Tac Toe : (board_size, win_length)
    *Rule: 
        + X = +1 
        + O = -1
        + Blank =0 
    *State : (board,player) , player: person about to take action
    *Action : blank to take : (row,col)
    """
    DIRECTIONS = (
        (0,1),
        (1,0),
        (1,1), #\
        (1,-1) #/

    )
    def __init__(self,size=3,win_length=3):
        if win_length > size:
            raise ValueError("win_length cannot > size")
        self.size = size 
        self.win_length = win_length

    def initial_state(self):
        board = tuple(tuple([0]*self.size) for _ in range(self.size))
        return (board,1) # X first

    def legal_actions(self,state):
        board,_ = state
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if board[r][c] == 0
        ]
    
    def candidate_actions(self, state, radius=None):
        """Blank pixels within `radius` of any placed stone.
        radius=None -> all legal actions. Empty board -> center pixel."""
        actions = self.legal_actions(state)
        if radius is None:
            return actions
        board, _ = state
        near_stone = set()
        has_stone = False
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] != 0:
                    has_stone = True
                    for near_r in range(max(0, row - radius), min(self.size, row + radius + 1)):
                        for near_c in range(max(0, col - radius), min(self.size, col + radius + 1)):
                            near_stone.add((near_r, near_c))
        if not has_stone:
            return [(self.size // 2, self.size // 2)]
        filtered = [a for a in actions if a in near_stone]
        return filtered or actions
    

    def next_state(self, state, action):
        board, player = state
        r, c = action
        if board[r][c] != 0:
            raise ValueError(f" Pixel {action} has already been chosen !")
        new_board = [list(row) for row in board]
        new_board[r][c] = player
        return (tuple(tuple(row) for row in new_board), -player)      

    def wins_at(self,board,r,c):
        """ True if (r,c) is in a loop-sequence >= win_length"""
        player = board[r][c]
        if player == 0 : 
            return False
        for dr,dc in self.DIRECTIONS:
            count = 1

            nr,nc = r + dr,c + dc
            while 0 <= nr < self.size and 0<= nc < self.size and board[nr][nc] == player: 
                count +=1 
                nr += dr 
                nc += dc 

            nr,nc = r-dr,c-dc
            while 0 <= nr <self.size and 0 <= nc < self.size and board[nr][nc] == player: 
                count +=1 
                nr -= dr
                nc -= dc

            if count >= self.win_length:
                return True 
        return False 

    def get_winner(self,state,last_action = None):
        board,_ = state 
        #Optimize
        if last_action is not None: 
            r,c = last_action 
            if self.wins_at(board,r,c):
                return board[r][c]
            else:
                return None 
        #Normal Brute Force
        else:
            for r in range(self.size):
                for c in range(self.size):
                    if self.wins_at(board,r,c):
                        return board[r][c]
            return None

    def is_full(self,state):
        board,_= state
        return all(cell !=0 for row in board for cell in row)

    def is_terminal(self, state,last_action = None):
        return self.get_winner(state,last_action) is not None or self.is_full(state)

    def rollout(self,state):
        #Edge case 
        winner = self.get_winner(state)
        if winner is not None:
            return winner 
        
        board = [list(row) for row in state[0]]
        player = state[1]
        empties = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if board[r][c] == 0
        ]
        random.shuffle(empties)

        for r, c in empties:
            board[r][c] = player
            if self.wins_at(board, r, c):
                return player
            player = -player
        return None     
        

    #VISUALIZATION
    def render(self, state):
        board, _ = state
        symbols = {1: "X", -1: "O", 0: "."}
        header = "   " + " ".join(f"{c:2d}" for c in range(self.size))
        lines = [header]
        for r in range(self.size):
            lines.append(f"{r:2d} " + " ".join(f" {symbols[v]}" for v in board[r]))
        return "\n".join(lines)

        

    
