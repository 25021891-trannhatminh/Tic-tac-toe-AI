from src.game import Game
from src.minimax import Minimax_Agent
g = Game(10, 5)
x_agent = Minimax_Agent(g, max_depth=3, radius=1)
o_agent = Minimax_Agent(g, max_depth=3, radius=1)

s = g.initial_state()
last = None
while not g.is_terminal(s, last):
    agent = x_agent if s[1] == 1 else o_agent   
    last = agent.best_move(s) #action to take , last_action leading to the future state
    s = g.next_state(s, last)
    print(g.render(s), "\n")

winner = g.get_winner(s, last)
print("Result :", {1: "X wins", -1: "O wins", None: "draw"}[winner])