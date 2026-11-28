from src.game import Game
from src.mcts import MCTS_Agent
#Test win random seed
game = Game(10, 5)
x_player = MCTS_Agent(game = game, seed = None,radius=2,rollout_type="heuristic")
o_player = MCTS_Agent(game = game, seed = None,radius=2,rollout_type="heuristic")

state = game.initial_state()
last = None
while not game.is_terminal(state, last):
    agent = x_player if state[1] == 1 else o_player   
    last = agent.best_move(state) 
    state = game.next_state(state, last)
    print(game.render(state), "\n")

winner = game.get_winner(state, last)
print("Result :", {1: "X wins", -1: "O wins", None: "draw"}[winner])