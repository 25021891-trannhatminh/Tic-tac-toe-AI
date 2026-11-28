from src.game import Game
from src.mcts import MCTS_Agent
import time 
#Test win random seed
game = Game(10, 5)
x_player = MCTS_Agent(game = game, seed = 36,radius=1,rollout_type="heuristic")
o_player = MCTS_Agent(game = game, seed = 36,radius=1,rollout_type="heuristic")

interval = float(input("Interval Input: ").strip())
state = game.initial_state()
last = None
while not game.is_terminal(state, last):
    #Changing first
    if state[1] ==1 :
        agent = o_player
    else:
        agent = x_player
     
    last = agent.best_move(state) 
    state = game.next_state(state, last)
    print(game.render(state), "\n")
    time.sleep(interval)

winner = game.get_winner(state, last)
print("Result :", {1: "X wins", -1: "O wins", None: "draw"}[winner])