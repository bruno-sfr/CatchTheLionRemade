from Game import LionBoard, Move
import math

class MCTS_Node:
    def __init__(self, parent, state: LionBoard.LionBoard, whiteTurn: bool, move: Move.Move):
        self.parent = parent
        self.children = []
        self.state = state
        self.whiteTurn = whiteTurn
        self.move = move
        self.score = 0
        self.visits = 0

    def backpropagete_value(self, value):
        self.score = self.score + value
        self.visits = self.visits + 1

    def propagete_value(self, value):
        self.score = self.score + value

    def add_child(self, child):
        self.children.append(child)

    def UCT(self):
        # source https://medium.com/@_michelangelo_/monte-carlo-tree-search-mcts-algorithm-for-dummies-74b2bae53bfa
        if self.visits == 0:
            return float('inf')
            #return 0

        """if self.parent == None:
            parent_visits = 1
        else:
            parent_visits = self.parent.visits"""

        parent = self
        if self.parent:
            parent = self.parent

        #C = math.sqrt(2)
        C = 0.7
        UCT = self.score / self.visits + C * math.sqrt(math.log(parent.visits)/self.visits)
        # print("UCT", UCT, " Children:", len(self.children))
        return UCT

    def printTree(self, depth:int):
        print("Depth:", depth, " Children:", len(self.children))
        for i in self.children:
            i.printTree(depth + 1)
