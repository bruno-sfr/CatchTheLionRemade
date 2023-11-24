import copy
import random
import sys
import time

from MonteCarlo import MCTS_Node
from Game import LionBoard, Move
from AlphaBeta import AlphaBeta
import signal
import multiprocessing

"""
MonteCarlo from https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/ and https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
UCT from https://www.chessprogramming.org/UCT
"""


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    # raise TimeoutError()
    raise TimeoutError("Function execution timed out.")


def MCTS(state: LionBoard, whiteTurn: bool, timeout_seconds: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        expanded_node = selection_including_Expansion(root)
        if expanded_node:
            result = simulation(expanded_node, whiteTurn)
            backpropagate(expanded_node, result)
        # --------------------------------
        else:
            # expanded node was terminal so run from root? / Backup for when expand node is null
            random_i = random.randint(0, len(root.children) - 1)
            result = simulation(root.children[random_i], whiteTurn)
            backpropagate(root.children[random_i], result)
            # result = simulation(root, whiteTurn)
            # backpropagate(root, result)
        # --------------------------------
    return best_child(root)


"""def MCTS_worker(state: LionBoard, whiteTurn: bool, root: MCTS_Node):
    while True:
        expanded_node = selection_including_Expansion(root)
        if expanded_node:
            result = simulation(expanded_node, whiteTurn)
            backpropagate(expanded_node, result)
        else:
            result = simulation(root, whiteTurn)
            backpropagate(root, result)


def MCTS(state: LionBoard, whiteTurn: bool, timeout_seconds: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    process = multiprocessing.Process(target=MCTS_worker, args=(state, whiteTurn, root))

    try:
        process.start()
        process.join(float(timeout_seconds))
    except multiprocessing.TimeoutError:
        process.terminate()
        print("Timeout expired.")
    else:
        process.join()
        print("Process completed.")
    return best_child(root)"""

"""
# main function for the Monte Carlo Tree Search
def MCTS(state: LionBoard, whiteTurn: bool, timeout_seconds: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)

    signal.signal(signal.SIGALRM, timeout_handler)
    #global timeout
    #timeout = True
    signal.alarm(timeout_seconds)
    try:
        #signal.alarm(timeout_seconds)
        while True:
        #print("timeout:", timeout)
        #while timeout:
            #print("timeout:", timeout)
            #selected_node = selection(root)
            #expanded_node = expansion(selected_node)
            expanded_node = selection_including_Expansion(root)
            if expanded_node:
                result = simulation(expanded_node, whiteTurn)
                backpropagate(expanded_node, result)
            #--------------------------------
            else:
                #expanded node was terminal so run from root?
                result = simulation(root, whiteTurn)
                backpropagate(root, result)
            #--------------------------------
            #if not (timeout):
            #    return best_child(root)
    except TimeoutError as e:
        print(e)
        #timeout = False
    finally:
        # Disable the alarm
        signal.alarm(0)

    best_node = best_child(root)
    #print("Visits:", best_node.visits)
    #print("Score:", best_node.score)
    return best_node

    # root.printTree(0)
    #print("Root Visits:", root.visits)
    #print("Root children:")
    #i2 = 1
    #for i in root.children:
    #    print("Root child", i2, " visits:", i.visits)
    #    i.move.printMove()
    #    i2 = i2 + 1
    #print("---------------------------------")
    #best_node = best_child(root)
    #print("Visits:", best_node.visits)
    #print("Score:", best_node.score)
    #return best_child(root)
"""


def MCTS_MR(state: LionBoard, whiteTurn: bool, timeout_seconds: int, depth: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        expanded_node = selection_including_Expansion(root)
        if expanded_node:
            result = MiniMax_Rollout(expanded_node, whiteTurn, depth)
            backpropagate(expanded_node, result)
        # --------------------------------
        else:
            # expanded node was terminal so run from root?
            random_i = random.randint(0, len(root.children) - 1)
            result = MiniMax_Rollout(root.children[random_i], whiteTurn, depth)
            backpropagate(root.children[random_i], result)
        # --------------------------------
    """print("Root Visits:", root.visits)
    print("Root children:")
    i2 = 1
    for i in root.children:
        print("Root child", i2, " visits:", i.visits)
        i.move.printMove()
        i2 = i2 + 1"""
    return best_child(root)


def MCTS_MS(state: LionBoard, whiteTurn: bool, timeout_seconds: int, depth: int, visit_threshold: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            expanded_node, result_index = selection_including_Expansion_with_MiniMax(root, whiteTurn, depth, visit_threshold)
        except TypeError as e:
            print(e)
        match result_index:
            case 0:
                # it already ran backpropagation in selection/expansion
                pass
            case 1:
                #result = MiniMax_Rollout(expanded_node, whiteTurn, depth)
                result = simulation(expanded_node, whiteTurn)
                backpropagate(expanded_node, result)
            case 2:
                random_i = random.randint(0, len(root.children) - 1)
                result = simulation(root.children[random_i], whiteTurn)
                backpropagate(root.children[random_i], result)

    return best_child(root)


"""def MCTS_MR(state: LionBoard, whiteTurn: bool, time, depth: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)

    timeout_seconds = time
    signal.signal(signal.SIGALRM, timeout_handler)
    timeout = False
    try:
        signal.alarm(timeout_seconds)

        while True:
            # selected_node = selection(root)
            # expanded_node = expansion(selected_node)
            expanded_node = selection_including_Expansion(root)
            if expanded_node:
                result = MiniMax_Rollout(expanded_node, whiteTurn, depth)
                backpropagate(expanded_node, result)
            if timeout:
                return best_child(root)
    except TimeoutError as e:
        print(e)
        timeout = True
        best_node = best_child(root)
        print("Visits:", best_node.visits)
        print("Score:", best_node.score)
        return best_node"""


def MCTS_MR_win_loss(state: LionBoard, whiteTurn: bool, time, depth: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)

    timeout_seconds = time
    signal.signal(signal.SIGALRM, timeout_handler)

    try:
        signal.alarm(timeout_seconds)

        while True:
            selected_node = selection(root)
            expanded_node = expansion(selected_node)
            result = MiniMax_Rollout_win_loss(expanded_node, whiteTurn, depth)
            backpropagate(expanded_node, result)
    except TimeoutError as e:
        print(e)

    # root.printTree(0)
    """print("Root Visits:", root.visits)
    print("Root children:")
    i2 = 1
    for i in root.children:
        print("Root child", i2, " visits:", i.visits)
        i2 = i2 + 1
    print("---------------------------------")"""
    return best_child(root)


def MCTS_full_expansion(state: LionBoard, whiteTurn: bool, time):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)

    timeout_seconds = time
    signal.signal(signal.SIGALRM, timeout_handler)

    try:
        signal.alarm(timeout_seconds)

        while True:
            selected_node = terminal_selection(root)
            expanded_node = complete_expansion(selected_node)
            result = simulation(expanded_node, whiteTurn)
            backpropagate(expanded_node, result)
    except TimeoutError as e:
        print(e)

    # root.printTree(0)
    """print("Root Visits:", root.visits)
    print("Root children:")
    i2 = 1
    for i in root.children:
        print("Root child", i2, " visits:", i.visits)
        i2 = i2 + 1
    print("---------------------------------")"""
    return best_child(root)


def selection_including_Expansion(node: MCTS_Node):
    move_list = node.state.allpossibleMoves_BigList(node.whiteTurn)
    # is there a not expanded move for this node?
    """if len(node.children) == 0:
        state = copy.deepcopy(node.state)
        try:
            move = state.makeRandomMove(node.whiteTurn)
        except Exception as e:
            print(e)
            #return node
            return None
        child = MCTS_Node.MCTS_Node(node, state, not (node.whiteTurn), move)
        node.add_child(child)
        return child"""
    # elif len(node.children) < len(move_list):
    if len(node.children) < len(move_list):
        # find move that is not expaned by iterationg over children
        for move in move_list:
            move_in_children = False
            for child in node.children:
                if child.move.equals(move):
                    move_in_children = True
            if move_in_children:
                continue
            else:
                # add node with move
                state = copy.deepcopy(node.state)
                state.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
                new_child = MCTS_Node.MCTS_Node(node, state, not (node.whiteTurn), move)
                node.add_child(new_child)
                return new_child
        """for move in move_list:
            for child in node.children:
                test = move.equals(child.move)
                if test:
                    continue
            else:
                # add node with move
                state = copy.deepcopy(node.state)
                state.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
                new_child = MCTS_Node.MCTS_Node(node, state, not (node.whiteTurn), move)
                node.add_child(new_child)
                return new_child
                break"""
    # else:
    elif len(node.children) > 0:
        best_child = node.children[0]
        for child in node.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        return selection_including_Expansion(best_child)
    else:
        # no move possible, is terminal node
        return None


def selection_including_Expansion_with_MiniMax(node: MCTS_Node, player: bool, depth: int, visit_threshold: int):
    # this func can have three different result, Mini-Max (0), expanded node(1), or terminal one(2)
    if node.visits >= visit_threshold:
        eval, moves = AlphaBeta.alpha_beta_win_loss_simple(depth, node.state, node.whiteTurn)
        # mcts plays for white
        if player:
            # shallow win/loss? then backpropaged result
            if eval == 1:
                # win
                backpropagate(node, 1)
                return node, 0
            elif eval == -1:
                # loss
                backpropagate(node, 0)
                return node, 0
        else:
            if eval == -1:
                backpropagate(node, 1)
                return node, 0
            elif eval == 1:
                backpropagate(node, 0)
                return node, 0

    move_list = node.state.allpossibleMoves_BigList(node.whiteTurn)
    # is there a not expanded move for this node?
    # elif len(node.children) < len(move_list):
    if len(node.children) < len(move_list):
        # find move that is not expaned by iterationg over children
        for move in move_list:
            move_in_children = False
            for child in node.children:
                if child.move.equals(move):
                    move_in_children = True
            if move_in_children:
                continue
            else:
                # add node with move
                state = copy.deepcopy(node.state)
                state.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
                new_child = MCTS_Node.MCTS_Node(node, state, not (node.whiteTurn), move)
                node.add_child(new_child)
                return new_child, 1
    # else:
    elif len(node.children) > 0:
        best_child = node.children[0]
        for child in node.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        result_node, result_index = node, 2
        try:
            result_node, result_index = selection_including_Expansion_with_MiniMax(best_child, player, depth, visit_threshold)
        except TypeError as e:
            print(e)
        return result_node, result_index
    else:
        # no move possible, is terminal node
        return node, 2


# selects next node to expand by comparing all existing nodes, also not termial ones
def selection(node: MCTS_Node):
    uct = node.UCT()
    best_UCT = uct
    best_node = node
    if node.children:
        for i in node.children:
            child = selection(i)
            child_UCT = child.UCT()
            if child_UCT > best_UCT:
                best_UCT = child_UCT
                best_node = child
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

    if len(list[0]) == 0 and len(list[1]) == 0 and len(list[2]) == 0 and len(list[3]) == 0 and len(
            list[4]) == 0 and len(list[5]) == 0:
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
    while i < MAX_ITERATIONS and not state.isGameOver():
        # while not state.isGameOver():
        try:
            state.makeRandomMove(whiteTurn)
        except Exception as e:
            print(e)
            if player == whiteTurn:
                return 0
            else:
                return 1
        whiteTurn = not whiteTurn
        i = i + 1

    if player and state.hasWhiteWon():
        return 1
    elif not player and state.hasBlackWon():
        return 1
    return 0


def MiniMax_Rollout(node: MCTS_Node, player: bool, depth: int):
    state = copy.deepcopy(node.state)
    whiteTurn = copy.deepcopy(node.whiteTurn)
    MAX_ITERATIONS = 50
    i = 0
    while i < MAX_ITERATIONS and not state.isGameOver():
        # while not state.isGameOver():
        # state.makeRandomMove(whiteTurn)
        eval, moves = AlphaBeta.alpha_beta_simple(depth, state, whiteTurn)
        # check if there are moves
        if len(moves) > 0:
            state.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo())
            whiteTurn = not whiteTurn
            i = i + 1
        else:
            return 0

    if player and state.hasWhiteWon():
        return 1
    elif not player and state.hasBlackWon():
        return 1
    return 0


def MiniMax_Rollout_win_loss(node: MCTS_Node, player: bool, depth: int):
    state = copy.deepcopy(node.state)
    whiteTurn = copy.deepcopy(node.whiteTurn)
    MAX_ITERATIONS = 100
    i = 0
    while i < MAX_ITERATIONS and not state.isGameOver:
        while not state.isGameOver():
            # state.makeRandomMove(whiteTurn)
            eval, moves = AlphaBeta.alpha_beta_win_loss_simple(depth, state, whiteTurn)
            state.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo())
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
    # sys.setrecursionlimit(5000)
    board = LionBoard.LionBoard()
    board.setBoard_start()
    #board.setBoard_Fen("e1g/1Cl/G11/1LE/")
    board.printBoard()

    print("")
    print("MCTS")
    result_node = MCTS(board, True, 3)
    result_node.move.printMove()
    print("Result node Children Count:", len(result_node.children))
    print("Visits:", result_node.visits)
    print("Score:", result_node.score)

    print("MCTS_MR")
    result_node = MCTS_MR(board, True, 3, 2)
    result_node.move.printMove()
    print("Result node Children Count:", len(result_node.children))
    print("Visits:", result_node.visits)
    print("Score:", result_node.score)

    print("MCTS-MS")
    result_node = MCTS_MS(board, True, 60, 3, 5)
    result_node.move.printMove()
    print("Result node Children Count:", len(result_node.children))
    print("Visits:", result_node.visits)
    print("Score:", result_node.score)

    """print("")
    print("MCTS_full_expansion")
    result_node = MCTS_full_expansion(board, True, 5)
    result_node.move.printMove()
    print("Result node Children Count:", len(result_node.children))
    print("Visits:", result_node.visits)
    print("Score:", result_node.score)"""

    """   list1 = [2,3,4,2]
        list2 = [2,3]
    
        for i1 in list1:
            for i2 in list2:
                if i1 == i2:
                    break
            else:
                print(i1)
                break"""
