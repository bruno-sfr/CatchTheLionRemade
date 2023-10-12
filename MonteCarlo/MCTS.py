import copy
import random

from MonteCarlo import MCTS_Node
from Game import LionBoard, Move
import signal
import math

"""
MonteCarlo from https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/ and https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
UCT from https://www.chessprogramming.org/UCT
"""


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out.")


# main function for the Monte Carlo Tree Search
def MCTS(state: LionBoard, whiteTurn: bool, time):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)

    timeout_seconds = time
    signal.signal(signal.SIGALRM, timeout_handler)

    try:
        signal.alarm(timeout_seconds)

        while True:
            #selected_node = selection(root)
            #expanded_node = expansion(selected_node)
            selected_node = terminal_selection(root)
            expanded_node = complete_expansion(selected_node)
            result = simulation(expanded_node, whiteTurn)
            backpropagate(expanded_node, result)
    except TimeoutError as e:
        print(e)

    #root.printTree(0)
    print("Root Visits:", root.visits)
    print("Root children:")
    for i in root.children:
        print("Root child visits:", i.visits)
    print("---------------------------------")
    return best_child(root)


# selects next node to expand by comparing all existing nodes, also not termial ones
def selection(node: MCTS_Node):
    uct = node.UCT()
    best_UCT = uct
    best_node = node
    if node.children:
        for i in node.children:
            best_child = selection(i)
            child_UCT = best_child.UCT()
            if child_UCT > best_UCT:
                best_UCT = child_UCT
                best_node = best_child
    return best_node

# selects node to expand via UCT, that is also Terminal
def terminal_selection(node: MCTS_Node):
    traverse_node = node

    while len(traverse_node.children) > 0:
        best_child = traverse_node.children[0]
        for child in traverse_node.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        traverse_node = best_child
    return traverse_node


# expands node by adding ONE child node
def expansion(node: MCTS_Node):
    state = copy.deepcopy(node.state)
    move = state.makeRandomMove(node.whiteTurn)
    child = MCTS_Node.MCTS_Node(node, state, not (node.whiteTurn), move)
    node.add_child(child)
    return child

# expands by adding all possible children and returns one of the children randomly
def complete_expansion(node: MCTS_Node):
    list = node.state.allpossibleMoves(node.whiteTurn)

    if  len(list[0]) == 0 and len(list[1]) == 0 and len(list[2]) == 0 and len(list[3]) == 0 and len(list[4]) == 0 and len(list[5]) == 0:
        # no possible moves
        return node

    for i in list:
        # print(len(i))
        for move in i:
            state = copy.deepcopy(node.state)
            state.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
            child = MCTS_Node.MCTS_Node(node, state, not (node.whiteTurn), move)
            node.add_child(child)

    if len(node.children) > 1:
        rand = random.randint(0, len(node.children) - 1)
        return node.children[rand]
    else:
        return node.children[0]

# plays random move until endstate or limit is reached
def simulation(node: MCTS_Node, player: bool):
    state = copy.deepcopy(node.state)
    whiteTurn = copy.deepcopy(node.whiteTurn)
    MAX_ITERATIONS = 100
    i = 0
    while i < MAX_ITERATIONS and not state.isGameOver:
        while not state.isGameOver():
            state.makeRandomMove(whiteTurn)
            whiteTurn = not whiteTurn
            i = i + 1

    if player and state.hasWhiteWon():
        return 1
    elif not player and state.hasBlackWon():
        return 1
    return 0


# function for backpropagation
def backpropagate(node: MCTS_Node, result):
    node.backpropagete_value(result)
    # root case
    if node.parent is not None:
        backpropagate(node.parent, result)
    else:
        return

    # function for selecting the best child


# node with highest number of visits
def best_child(node: MCTS_Node):
    best_child = node.children[0]
    for i in node.children:
        if i.visits > best_child.visits:
            best_child = i
    return best_child


if __name__ == '__main__':
    board = LionBoard.LionBoard()
    board.setBoard_start()
    result_node = MCTS(board, True, 10)
    print(result_node.move.printMove())
    print("Result node Children Count:", len(result_node.children))
    print("Visits:", result_node.visits)
    print("Score:", result_node.score)
