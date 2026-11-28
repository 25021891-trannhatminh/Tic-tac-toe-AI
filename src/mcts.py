import math
import random
from .heuristic_rollout_OPTIMAL import heuristic_rollout

class Node:
    def __init__(self, state, parent=None, action=None, game=None, radius=None):
        self.state = state                   # current state = (board,player)
        self.parent = parent
        self.action = action                 # last action của Parent Node
        self.childrens = []                  # list Child Node
        self.N = 0                           # số lần thăm Node
        self.W = 0.0                         # số lần win Node khi simulate
        self.parent_player = - state[1]      # Player từ Parent (NOTE: Do W = số lần win nếu parent_player chọn Node này -> winner_simulate = parent_player)

        # Check game done ?
        if action is not None:
            self.winner = game.get_winner(state, action)
        else:
            self.winner = game.get_winner(state)
        self.is_terminal = (self.winner is not None) or game.is_full(state)

        # Create new actions []
        if self.is_terminal:
            self.untried_actions = []
        else:
            actions = game.candidate_actions(state,radius)
            """
            If there is a win-now move in actions , prioring it first
            """
            win_move = None
            board,player = state 
            board_copy = [list(r) for r in board]
            for row, col in actions:
                board_copy[row][col] = player
                if game.wins_at(board_copy,row,col):
                    win_move = (row,col)
                    break 
                board_copy[row][col] = 0
            self.untried_actions =[win_move] if win_move else actions
        random.shuffle(self.untried_actions)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def uct_value(self, const):
        if self.N == 0:
            return float("inf")
        exploit = self.W / self.N
        explore = const * math.sqrt(math.log(self.parent.N) / self.N)
        return exploit + explore


class MCTS_Agent:
    def __init__(self, game, iterations=1000, c=math.sqrt(2), seed=None, radius=None, rollout_type = "random"):
        """
        game       : Game Object
        iterations : số vòng lặp MCTS cho mỗi nước đi
        c          : const = sqrt(2)
        seed       : đặt seed lặp lại kết quả (để test)
        radius     : None = xét mọi ô trống; số = chỉ xét ô cách quân đã đánh <= radius
        """
        self.game = game
        self.radius = radius
        self.iterations = iterations
        self.c = c
        self.root = None
        self.rollout_type = rollout_type
        if seed is not None:
            random.seed(seed)

    # SELECT - EXPAND - SIMULATE - BACKPROPAGATE
    def _select(self, node):
        """1. Traverse DFS theo UCT từ `node` -> Leaf """
        while not node.is_terminal:
            if not node.is_fully_expanded():
                return node
            node = max(node.childrens, key=lambda child_node: child_node.uct_value(self.c))
        return node

    def _expand(self, node):
        """2. Expand 1 new Node from untried actions """
        if node.is_terminal:
            return node
        action = node.untried_actions.pop()
        child_state = self.game.next_state(node.state, action)
        child_node = Node(child_state, parent=node, action=action, game=self.game, radius=self.radius)
        node.childrens.append(child_node)
        return child_node

    def _simulate(self, node):
        """3. Simulate a game until end + Return winner/None"""
        if node.is_terminal:
            return node.winner
        if self.rollout_type == "heuristic":
            return heuristic_rollout(self.game, node.state)
        else: # self.rollout_type == "random"
            return self.game.rollout(node.state)

    def _backpropagate(self, node, winner):
        """4. Update W,N from leaf to root"""
        while node is not None:
            node.N += 1
            if winner is None:
                node.W += 0.5
            elif winner == node.parent_player:
                node.W += 1.0
            node = node.parent

    # Combination
    def best_move(self, state):
        """Chạy MCTS từ `state`, return action = (row, col) có số lần thăm lớn nhất."""
        self.root = Node(state, game=self.game, radius=self.radius)
        if self.root.is_terminal:
            raise ValueError("State is terminal")

        for _ in range(self.iterations):
            leaf = self._select(self.root)
            leaf = self._expand(leaf)
            winner = self._simulate(leaf)
            self._backpropagate(leaf, winner)

        best_node = max(self.root.childrens, key=lambda ch: ch.N)
        return best_node.action

    # def root_stats(self):
    #     """Bảng thống kê các con của root: action, N, W, W/N (sắp theo N giảm dần)."""
    #     rows = []
    #     for ch in self.root.childrens:
    #         rows.append({
    #             "action": ch.action,
    #             "N": ch.N,
    #             "W": ch.W,
    #             "W/N": ch.W / ch.N if ch.N else 0.0,
    #         })
    #     return sorted(rows, key=lambda r: r["N"], reverse=True)

