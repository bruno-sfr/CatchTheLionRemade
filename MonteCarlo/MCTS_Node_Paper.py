from Game import LionBoard, Move
import math

class MCTS_Node_Paper:
    def __init__(self, parent, state: LionBoard.LionBoard, whiteTurn: bool, move: Move.Move):
        self.parent = parent
        self.children = []
        self.state = state
        self.whiteTurn = whiteTurn
        self.move = move
        self.score = 0
        self.visits = 0

    def add_value(self, value):
        self.score = self.score + value

    def add_child(self, child):
        self.children.append(child)

    def UCT(self):
        # source https://medium.com/@_michelangelo_/monte-carlo-tree-search-mcts-algorithm-for-dummies-74b2bae53bfa
        if self.visits == 0:
            return float('inf')

        parent = self
        if self.parent:
            parent = self.parent

        C = 0.7
        """ADDED Minus as Test"""
        UCT = -self.score / self.visits + math.sqrt(C * math.log(parent.visits)/self.visits)
        return UCT

    def printTree(self, depth:int):
        print("Depth:", depth, " Children:", len(self.children))
        for i in self.children:
            i.printTree(depth + 1)
