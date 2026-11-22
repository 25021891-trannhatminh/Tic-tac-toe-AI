import math as m
import numpy as np

class Minimax_Agent:
    """
    MiniMax / Alpha_Beta for (game_size,win_length )
    use_alpha_beta: False = MiniMax, True = Alpha_Beta_Pruning
    max_depth = None: Brute Force (3 x 3)
                int : Limited Depth, then call Heuristic Function
    radius = None: Brute Force
            int:  only pixels ( <= radius ) just taken pixel
    """
    WIN = 100_000 
    def __init__(self,game,use_alpha_beta=True,max_depth = None,radius = None):
        self.game = game 
        self.use_alpha_beta = use_alpha_beta 
        self.max_depth = max_depth
        self.radius = radius 
        self.nodes = 0 
    def best_move(self,state):
        """Return best move for the player taking turn """
        self.nodes =0 
        player =state[1]
        best_action, best_value = None, -m.inf
        alpha,beta = -m.inf, m.inf
        depth = self.max_depth if self.max_depth is not None else m.inf 
        for action in self.ordered_actions(state):
            child = self.game.next_state(state,action)
            value = self.search(child,depth-1,alpha,beta,action, player)
            if value > best_value:
                best_value,best_action = value,action
            if self.use_alpha_beta:
                alpha = max(alpha,best_value)
        return best_action

    def search(self,state,depth,alpha,beta,last_action,player):
        """Value of state , POV of player (calling best_move )"""
        self.nodes +=1 
        game = self.game
        winner = game.get_winner(state,last_action)
        if winner is not None: 
            bonus = depth if depth != m.inf else 0 
            if winner == player: 
                return self.WIN + bonus 
            else:
                return -(self.WIN+ bonus)

        if game.is_full(state):
            return 0 
        if depth <= 0:
            #Heuristic Fuction 
            return self.evaluate(state,player)

        #Alpha-Beta Pruning 
        if state[1] == player:
            is_max = True 
        else:
            is_max = False 
        actions = self.ordered_actions(state)
        if is_max: 
            best = -m.inf
            for action in actions: 
                child = game.next_state(state,action)
                value = self.search(child,depth-1,alpha,beta,action,player)
                best = max(best,value)
                #Alpha Pruning 
                if self.use_alpha_beta: 
                    alpha = max(alpha,best)
                    if alpha >= beta:
                        break
            return best 
        else:
            best = m.inf
            for action in actions:
                child = game.next_state(state,action)
                value = self.search(child,depth-1,alpha,beta,action,player)
                best = min(best,value)
                # Beta Pruning
                if self.use_alpha_beta:
                    beta = min(beta,best)
                    if alpha >= beta:
                        break 
            return best 

    def ordered_actions(self,state):
        """
        + Get legit list of actions 
        + Limit pixels with radius --> Trade Off
        + Sorting actions --> Alpha-Beta if better at Pruning: Early detection on pruning condition #Optimization
            Bias : Board Centroid<Base>  #Heuristic: Expansion Opportunity
        """
        game, board = self.game, state[0]
        actions = game.legal_actions(state)

        if self.radius is not None: 
            stones = [(r,c) for r in range(game.size) for c in range(game.size)
                      if board[r][c] != 0 ] # Pixel (has already been taken)
            if not stones: 
                return [(game.size//2,game.size//2)]
            near = [action for action in actions
                    if any(max(abs(action[0]-r), abs(action[1]-c))<= self.radius for r,c in stones)]
            
            if near:
                actions = near 
            else:
                actions = actions 

        #Optimization: Sorting from Centroid of the board to Edge 
        mid = (game.size-1)//2 #(mid,mid) = centroid
        actions.sort(key= lambda a: abs(a[0]-mid)+ abs(a[1]-mid))
        return actions 
            
    #Heutistic Fuction: Evaluating when max_depth is reached
    def evaluate(self,state,player):
        game,board = self.game, state[0]
        n,k = game.size, game.win_length 
        score = 0.0 

        for dr, dc in game.DIRECTIONS: 
            for r in range(n):
                for c in range(n):
                    end_r = r + dr*(k-1)
                    end_c = c + dc*(k-1)
                    if not (0 <= end_r < n and 0<= end_c<n):
                        continue 

                    of_player = of_opponent = 0 
                    for i in range(k):
                        value = board[r+dr*i][c+dc*i]
                        if value == player: 
                            of_player +=1 
                        elif value != 0: 
                            of_opponent += 1

                    if of_player and  not of_opponent :
                        score += 10 ** of_player
                    if of_opponent and not of_player: 
                        score -= 10**of_opponent
        return score 






        


            
             

         
        

