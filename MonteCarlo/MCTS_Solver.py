import copy
import math
import random
import sys
import time

from MonteCarlo import MCTS_Node
from Game import LionBoard, Move
from AlphaBeta import AlphaBeta
import signal

"""def MCTS_Paper_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_Paper(root)
    return secure_child(root)

def MCTS_Paper(N: MCTS_Node):
#Integer MCTSSolver(Node N){
    if N.state.isGameOver():
        if N.whiteTurn:
            if N.state.hasWhiteWon():
                # player to move wins
                return float('inf')
            else:
                # player to move losses
                return float('-inf')
        else:
            if N.state.hasBlackWon():
                # player to move wins
                return float('inf')
            else:
                # player to move losses
                return float('-inf')
#    if (playerToMoveWins(N))
#        return INFINITY
#    else if (playerToMoveLoses(N))
#        return -INFINITY

    best_child = select_Paper(N)
    N.visits = N.visits + 1
#    bestChild = select(N)
#    N.visitCount++

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child, best_child.whiteTurn)
            best_child.visits = 1
            N.add_child(best_child)
            N.backpropagete_value(R)
            return R
        else:
            R = -MCTS_Paper(best_child)
    else:
        R = best_child.score
#    if (bestChild.value != -INFINITY AND bestChild.value != INFINITY) {
#        if (bestChild.visitCount == 0) {
#            R = -playOut(bestChild)
#            addToTree(bestChild)
#            goto DONE
#        }
#        } else {
#            R = -MCTSSolver(bestChild)
#        }
#    else
#        R = bestChild.value

    if R == float('inf'):
        N.score = float('-inf')
        return R
    elif R == float('-inf'):
        for child in N.children:
            if child.score != R:
                R = -1
                N.backpropagete_value(R)
                return R
        N.score = float('inf')
        return R
    else:
        N.backpropagete_value(R)
        return R
#    if (R == INFINITY) {
#        N.value = -INFINITY
#        return R
#    } else if (R == -INFINITY) {
#        foreach (child in getChildren(N)) {
#            if (child.value != R) {
#                R = -1
#                goto DONE
#            }
#        }
#        N.value = INFINITY
#        return R
#    }

#DONE:
#    N.computeAverage(R)
#    return R
#}


def select_Paper(N:MCTS_Node):
    move_list = N.state.allpossibleMoves_BigList(N.whiteTurn)
    if len(N.children) < len(move_list):
        # find move that is not expaned by iterationg over children
        for move in move_list:
            move_in_children = False
            for child in N.children:
                if child.move.equals(move):
                    move_in_children = True
            if move_in_children:
                continue
            else:
                # add node with move
                state = copy.deepcopy(N.state)
                state.makeMove(N.whiteTurn, move.getFrom(), move.getTo())
                new_child = MCTS_Node.MCTS_Node(N, state, not N.whiteTurn, move)
                #N.add_child(new_child)
                return new_child
    elif len(N.children) > 0:
        best_child = N.children[0]
        for child in N.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        return best_child
    else:
        # no move possible, is terminal node
        # print("Terminal Node")
        return None
"""
def MCTS_Solver(state: LionBoard, whiteTurn: bool, timeout_seconds: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        # expanded_node = selection_including_Expansion_Solver(root, whiteTurn)
        expanded_node = selection_including_Expansion_Solver_NegaMax(root, whiteTurn)
        #expanded_node = selection_including_Expansion_Solver_MiniMax(root, whiteTurn)
        if expanded_node:
            result = simulation(expanded_node, whiteTurn)
            # backpropagate_Solver(expanded_node, result)
            backpropagate_Solver_NegaMax(expanded_node, result)
            #backpropagate_Solver_MiniMax(expanded_node, result)
        # --------------------------------
        else:
            # expanded node was terminal so run from root? / Backup for when expand node is null
            pass
            # random_i = random.randint(0, len(root.children) - 1)
            # result = simulation(root.children[random_i], whiteTurn)
            # backpropagate(root.children[random_i], result)
            # result = simulation(root, whiteTurn)
            # backpropagate(root, result)
        # --------------------------------
    return secure_child(root)


def MCTS_MR_Solver(state: LionBoard, whiteTurn: bool, timeout_seconds: int, depth: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        expanded_node = selection_including_Expansion_Solver_NegaMax(root, whiteTurn)
        #expanded_node = selection_including_Expansion_Solver_MiniMax(root, whiteTurn)
        if expanded_node:
            result = MiniMax_Rollout(expanded_node, whiteTurn, depth)
            # result = MiniMax_Rollout_win_loss(expanded_node, whiteTurn, depth)
            backpropagate_Solver_NegaMax(expanded_node, result)
            #backpropagate_Solver_MiniMax(expanded_node, result)
    """print("Root Visits:", root.visits)
    print("Root children:")
    i2 = 1
    for i in root.children:
        print("Root child", i2, " visits:", i.visits)
        i.move.printMove()
        i2 = i2 + 1"""
    return secure_child(root)


def MCTS_MS_Solver(state: LionBoard, whiteTurn: bool, timeout_seconds: int, depth: int, visit_threshold: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        #expanded_node = selection_including_Expansion_Solver_MiniMax(root, whiteTurn, depth, visit_threshold)
        expanded_node = selection_including_Expansion_Solver_MiniMax_MS(root, whiteTurn, depth, visit_threshold)

        # got expanded node
        if expanded_node:
            result = simulation(expanded_node, whiteTurn)
            backpropagate_Solver_MiniMax(expanded_node, result)
    print("Root Visits:", root.visits)
    return secure_child(root)


def selection_including_Expansion_Solver(node: MCTS_Node, whiteTurn: bool):
    move_list = node.state.allpossibleMoves_BigList(node.whiteTurn)

    # if node.score == float('inf') or node.score == float('-inf'):
    #    backpropagate_Solver(node, node.score)

    if node.state.isGameOver():
        # print("Terminal Node")
        # terminal node so propagate proven win/proven loss
        if whiteTurn:
            if node.state.hasWhiteWon():
                # the player is white and has won so propagate win
                backpropagate_Solver(node, float('inf'))
            else:
                backpropagate_Solver(node, float('-inf'))
        else:
            if node.state.hasBlackWon():
                # the player is black and has won so propagate win
                backpropagate_Solver(node, float('inf'))
            else:
                backpropagate_Solver(node, float('-inf'))

    if node.score == float('inf') or node.score == float('-inf'):
        # detect proven win
        backpropagate_Solver(node, node.score)
        return
    # elif len(node.children) < len(move_list):
    elif len(node.children) < len(move_list):
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
    # else:
    # elif node.score == float('inf') or node.score == float('-inf'):
    # detect proven win
    #    backpropagate_Solver(node, node.score)
    elif len(node.children) > 0:
        best_child = node.children[0]
        for child in node.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        return selection_including_Expansion_Solver(best_child, whiteTurn)
    else:
        # no move possible, is terminal node
        # print("Terminal Node")
        return None


def selection_including_Expansion_Solver_NegaMax(node: MCTS_Node, whiteTurn: bool):
    move_list = node.state.allpossibleMoves_BigList(node.whiteTurn)

    # if node.score == float('inf') or node.score == float('-inf'):
    #    backpropagate_Solver(node, node.score)

    if node.state.isGameOver():
        # print("Terminal Node")
        # terminal node so propagate proven win/proven loss
        # if whiteTurn:
        if node.whiteTurn:
            if node.state.hasWhiteWon():
                # the player is white and has won so propagate win
                node.backpropagete_value(float('inf'))
                backpropagate_Solver_NegaMax(node.parent, float('inf'))
            else:
                node.backpropagete_value(float('-inf'))
                backpropagate_Solver_NegaMax(node.parent, float('-inf'))
        else:
            if node.state.hasBlackWon():
                # the player is black and has won so propagate win
                node.backpropagete_value(float('inf'))
                backpropagate_Solver_NegaMax(node.parent, float('inf'))
            else:
                node.backpropagete_value(float('-inf'))
                backpropagate_Solver_NegaMax(node.parent, float('-inf'))
        return

    if node.score == float('inf') or node.score == float('-inf'):
        # detect proven win
        backpropagate_Solver_NegaMax(node.parent, node.score)
        return
    """if len(node.children) == 0 and len(move_list) > 0:
        # node is leaf with possible moves
        for move in move_list:
            check_board = copy.deepcopy(node.state)
            check_board.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
            if check_board.isGameOver():
                if not(node.whiteTurn):
                    if check_board.hasWhiteWon():
                        # the player is white and has won so propagate win
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        new_child.backpropagete_value(float('inf'))
                        backpropagate_Solver_NegaMax(node, float('inf'))
                        return
                        #backpropagate_Solver_NegaMax(new_child, float('inf'))
                    else:
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        new_child.backpropagete_value(float('-inf'))
                        #backpropagate_Solver_NegaMax(new_child, float('-inf'))
                else:
                    if check_board.hasBlackWon():
                        # the player is black and has won so propagate win
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        new_child.backpropagete_value(float('inf'))
                        backpropagate_Solver_NegaMax(node, float('inf'))
                        return
                        #backpropagate_Solver_NegaMax(new_child, float('inf'))
                    else:
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        new_child.backpropagete_value(float('-inf'))
                        #backpropagate_Solver_NegaMax(new_child, float('-inf'))
                return"""
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
    # else:
    # elif node.score == float('inf') or node.score == float('-inf'):
    # detect proven win
    #    backpropagate_Solver(node, node.score)
    elif len(node.children) > 0:
        best_child = node.children[0]
        for child in node.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        return selection_including_Expansion_Solver_NegaMax(best_child, whiteTurn)
    else:
        # no move possible, is terminal node
        # print("Terminal Node")
        return None


def selection_including_Expansion_Solver_MiniMax(node: MCTS_Node, whiteTurn: bool):
    move_list = node.state.allpossibleMoves_BigList(node.whiteTurn)

    # if node.score == float('inf') or node.score == float('-inf'):
    #    backpropagate_Solver(node, node.score)

    if node.state.isGameOver():
        # print("Terminal Node")
        # terminal node so propagate proven win/proven loss
        # if whiteTurn:
        if whiteTurn:
            if node.state.hasWhiteWon():
                # the player is white and has won so propagate win
                backpropagate_Solver_MiniMax(node, float('inf'))
            else:
                backpropagate_Solver_MiniMax(node, float('-inf'))
        else:
            if node.state.hasBlackWon():
                # the player is black and has won so propagate win
                backpropagate_Solver_MiniMax(node, float('inf'))
            else:
                backpropagate_Solver_MiniMax(node, float('-inf'))
        return

    if node.score == float('inf') or node.score == float('-inf'):
        # detect proven win
        backpropagate_Solver_MiniMax(node, node.score)
        return
    if len(node.children) == 0 and len(move_list) > 0:
        # node is leaf with possible moves
        for move in move_list:
            check_board = copy.deepcopy(node.state)
            check_board.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
            if check_board.isGameOver():
                if whiteTurn:
                    if check_board.hasWhiteWon():
                        # the player is white and has won so propagate win
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_MiniMax(new_child, float('inf'))
                    else:
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_MiniMax(new_child, float('-inf'))
                else:
                    if check_board.hasBlackWon():
                        # the player is black and has won so propagate win
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_MiniMax(new_child, float('inf'))
                    else:
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_MiniMax(new_child, float('-inf'))
                return
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
    # else:
    # elif node.score == float('inf') or node.score == float('-inf'):
    # detect proven win
    #    backpropagate_Solver(node, node.score)
    elif len(node.children) > 0:
        best_child = node.children[0]
        for child in node.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        return selection_including_Expansion_Solver_MiniMax(best_child, whiteTurn)
    else:
        # no move possible, is terminal node
        # print("Terminal Node")
        return None


def selection_including_Expansion_Solver_MiniMax_MS(node: MCTS_Node, whiteTurn: bool, depth: int, visit_threshold: int):
    move_list = node.state.allpossibleMoves_BigList(node.whiteTurn)

    # if node.score == float('inf') or node.score == float('-inf'):
    #    backpropagate_Solver(node, node.score)

    if node.state.isGameOver():
        # print("Terminal Node")
        # terminal node so propagate proven win/proven loss
        # if whiteTurn:
        if whiteTurn:
            if node.state.hasWhiteWon():
                # the player is white and has won so propagate win
                backpropagate_Solver_MiniMax(node, float('inf'))
            else:
                backpropagate_Solver_MiniMax(node, float('-inf'))
        else:
            if node.state.hasBlackWon():
                # the player is black and has won so propagate win
                backpropagate_Solver_MiniMax(node, float('inf'))
            else:
                backpropagate_Solver_MiniMax(node, float('-inf'))
        return

    if node.score == float('inf') or node.score == float('-inf'):
        # detect proven win
        backpropagate_Solver_MiniMax(node, node.score)
        return
    if len(node.children) == 0 and len(move_list) > 0:
        # node is leaf with possible moves
        for move in move_list:
            check_board = copy.deepcopy(node.state)
            check_board.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
            if check_board.isGameOver():
                if whiteTurn:
                    if check_board.hasWhiteWon():
                        # the player is white and has won so propagate win
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_MiniMax(new_child, float('inf'))
                    else:
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_MiniMax(new_child, float('-inf'))
                else:
                    if check_board.hasBlackWon():
                        # the player is black and has won so propagate win
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_MiniMax(new_child, float('inf'))
                    else:
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_MiniMax(new_child, float('-inf'))
                return
    if node.visits >= visit_threshold:
        for move in move_list:
            check_board = copy.deepcopy(node.state)
            check_board.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
            eval, moves = AlphaBeta.alpha_beta_win_loss_simple(depth, check_board, not (node.whiteTurn))
            # mcts plays for white
            if whiteTurn:
                # shallow win/loss? then backpropaged result
                if eval == 1:
                    # win
                    new_child = MCTS_Node.MCTS_Node(node, check_board, not node.whiteTurn, move)
                    node.add_child(new_child)
                    backpropagate_Solver_MiniMax(new_child, float('inf'))
                    return
                elif eval == -1:
                    # loss
                    new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                    node.add_child(new_child)
                    backpropagate_Solver_MiniMax(new_child, float('-inf'))
                    #return
            else:
                if eval == -1:
                    new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                    node.add_child(new_child)
                    backpropagate_Solver_MiniMax(new_child, float('inf'))
                    return
                elif eval == 1:
                    new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                    node.add_child(new_child)
                    backpropagate_Solver_MiniMax(new_child, float('-inf'))
                    # return
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
    # else:
    # elif node.score == float('inf') or node.score == float('-inf'):
    # detect proven win
    #    backpropagate_Solver(node, node.score)
    elif len(node.children) > 0:
        best_child = node.children[0]
        for child in node.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        return selection_including_Expansion_Solver_MiniMax(best_child, whiteTurn)
    else:
        # no move possible, is terminal node
        # print("Terminal Node")
        return None


"""def selection_including_Expansion_Solver_MS(node: MCTS_Node, whiteTurn: bool, depth: int, visit_threshold: int):
    move_list = node.state.allpossibleMoves_BigList(node.whiteTurn)

    # if node.score == float('inf') or node.score == float('-inf'):
    #    backpropagate_Solver(node, node.score)

    if node.state.isGameOver():
        # print("Terminal Node")
        # terminal node so propagate proven win/proven loss
        # if whiteTurn:
        if node.whiteTurn:
            if node.state.hasWhiteWon():
                # the player is white and has won so propagate win
                backpropagate_Solver_NegaMax(node, float('inf'))
            else:
                backpropagate_Solver_NegaMax(node, float('-inf'))
        else:
            if node.state.hasBlackWon():
                # the player is black and has won so propagate win
                backpropagate_Solver_NegaMax(node, float('inf'))
            else:
                backpropagate_Solver_NegaMax(node, float('-inf'))
        return

    if node.score == float('inf') or node.score == float('-inf'):
        # detect proven win
        backpropagate_Solver_NegaMax(node, node.score)
        return
    if node.visits >= visit_threshold:
        for move in move_list:
            check_board = copy.deepcopy(node.state)
            check_board.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
            eval, moves = AlphaBeta.alpha_beta_win_loss_simple(depth, check_board, not (node.whiteTurn))
            # mcts plays for white
            if node.whiteTurn:
                # shallow win/loss? then backpropaged result
                if eval == 1:
                    # win
                    new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                    node.add_child(new_child)
                    backpropagate_Solver_NegaMax(new_child, float('inf'))
                    return None
                elif eval == -1:
                    # loss
                    new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                    node.add_child(new_child)
                    backpropagate_Solver_NegaMax(new_child, float('-inf'))
                    return None
            else:
                if eval == -1:
                    new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                    node.add_child(new_child)
                    backpropagate_Solver_NegaMax(new_child, float('inf'))
                    return None
                elif eval == 1:
                    new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                    node.add_child(new_child)
                    backpropagate_Solver_NegaMax(new_child, float('-inf'))
                    return None
    if len(node.children) == 0 and len(move_list) > 0:
        # node is leaf with possible moves
        for move in move_list:
            check_board = copy.deepcopy(node.state)
            check_board.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
            if check_board.isGameOver():
                if node.whiteTurn:
                    if check_board.hasWhiteWon():
                        # the player is white and has won so propagate win
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_NegaMax(new_child, float('inf'))
                    else:
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_NegaMax(new_child, float('-inf'))
                else:
                    if check_board.hasBlackWon():
                        # the player is black and has won so propagate win
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_NegaMax(new_child, float('inf'))
                    else:
                        new_child = MCTS_Node.MCTS_Node(node, check_board, not (node.whiteTurn), move)
                        node.add_child(new_child)
                        backpropagate_Solver_NegaMax(new_child, float('-inf'))
                return
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
    # else:
    # elif node.score == float('inf') or node.score == float('-inf'):
    # detect proven win
    #    backpropagate_Solver(node, node.score)
    elif len(node.children) > 0:
        best_child = node.children[0]
        for child in node.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        return selection_including_Expansion_Solver_MiniMax(best_child, whiteTurn, depth, visit_threshold)
    else:
        # no move possible, is terminal node
        # print("Terminal Node")
        return None
"""

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
    MAX_ITERATIONS = 25
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


def backpropagate_Solver(node: MCTS_Node, result):
    if result == float('inf'):
        # proven win
        proven = True
        for child in node.children:
            if child.score != float('inf'):
                proven = False
                break
        if not proven:
            # child is not proven win so propate normal win
            node.backpropagete_value(1)
            if node.parent is not None:
                backpropagate_Solver(node.parent, 1)
            # else:
            #    return
            return
    elif result == float('-inf'):
        # proven win
        proven = True
        for child in node.children:
            if child.score != float('-inf'):
                proven = False
                break
        if not proven:
            # child is not proven loss so propate normal loss
            node.backpropagete_value(-1)
            if node.parent is not None:
                backpropagate_Solver(node.parent, -1)
            # else:
            #    return
            return

    node.backpropagete_value(result)
    # root case
    if node.parent is not None:
        backpropagate_Solver(node.parent, result)
    else:
        return


def backpropagate_Solver_NegaMax(node: MCTS_Node, result):
    if result == float('inf'):
        # proven win since negamax one child is enough for -inf so
        node.backpropagete_value(float('-inf'))
        if node.parent is not None:
            backpropagate_Solver_NegaMax(node.parent, float('-inf'))
        return
    elif result == float('-inf'):
        # proven win
        proven = True
        for child in node.children:
            if child.score != float('-inf'):
                proven = False
                break
        if not proven:
            # child is not proven loss so propate normal loss
            node.backpropagete_value(-1)
            if node.parent is not None:
                backpropagate_Solver_NegaMax(node.parent, -1)
            return
        else:
            # all children are proven loss so negamax inf
            node.backpropagete_value(float('inf'))
            if node.parent is not None:
                backpropagate_Solver_NegaMax(node.parent, float('inf'))
            return
    else:
        node.backpropagete_value(result)
        # root case
        if node.parent is not None:
            backpropagate_Solver_NegaMax(node.parent, result)
        return


def backpropagate_Solver_MiniMax(node: MCTS_Node, result):
    if result == float('inf'):
        # proven win since minimax one child is enough for inf so
        node.backpropagete_value(float('inf'))
        if node.parent is not None:
            backpropagate_Solver_MiniMax(node.parent, float('inf'))
        return
    elif result == float('-inf'):
        # proven loss of child, check if node also proven loss
        proven = True
        for child in node.children:
            if child.score != float('-inf'):
                #child score not -inf so not proven loss
                proven = False
                break

        if not proven:
            # child is not proven loss so propate normal loss
            node.backpropagete_value(-1)
            if node.parent is not None:
                backpropagate_Solver_MiniMax(node.parent, -1)
            return
        else:
            # all children are proven loss so minimax -inf
            node.backpropagete_value(float('-inf'))
            if node.parent is not None:
                backpropagate_Solver_MiniMax(node.parent, float('-inf'))
            return
    else:
        node.backpropagete_value(result)
        # root case
        if node.parent is not None:
            backpropagate_Solver_MiniMax(node.parent, result)
        return


def backpropagate_Solver_MiniMax_MB(node: MCTS_Node, result, whiteTurn: bool, depth: int):
    if result == float('inf'):
        # proven win since minimax one child is enough for inf so
        node.backpropagete_value(float('inf'))
        if node.parent is not None:
            backpropagate_Solver(node.parent, float('inf'))
        return
    elif result == float('-inf'):
        # proven loss of child, check if node also proven loss
        proven = True
        for child in node.children:
            if child.score != float('-inf'):
                #child score not -inf so not proven loss
                check_board = copy.deepcopy(child.state)
                eval, moves = AlphaBeta.alpha_beta_win_loss_simple(depth, check_board, child.whiteTurn)
                if whiteTurn:
                    # shallow win/loss? then backpropaged result
                    if eval == 1:
                        # found win
                        backpropagate_Solver_MiniMax_MB(child, float('inf'), whiteTurn, depth)
                        return
                    elif eval == -1:
                        # found loss so contiune checking for proven loss
                        child.backpropagete_value(float('-inf'))
                        # return
                    else:
                        # not proven
                        proven = False
                        break
                else:
                    if eval == -1:
                        backpropagate_Solver_MiniMax_MB(child, float('inf'), whiteTurn, depth)
                        return
                    elif eval == 1:
                        child.backpropagete_value(float('-inf'))
                    else:
                        # not proven
                        proven = False
                        break
                #proven = False
                #break

        if not proven:
            # child is not proven loss so propate normal loss
            node.backpropagete_value(-1)
            if node.parent is not None:
                backpropagate_Solver_MiniMax_MB(node.parent, -1, whiteTurn, depth)
            return
        else:
            # all children are proven loss so minimax -inf
            node.backpropagete_value(float('-inf'))
            if node.parent is not None:
                backpropagate_Solver_MiniMax_MB(node.parent, float('-inf'), whiteTurn, depth)
            return
    else:
        node.backpropagete_value(result)
        # root case
        if node.parent is not None:
            backpropagate_Solver_MiniMax_MB(node.parent, result, whiteTurn, depth)
        return


def secure_child(node: MCTS_Node):
    A = 1
    best_child = node.children[0]
    best_eval = best_child.score + A / math.sqrt(best_child.visits)
    for i in node.children:
        new_eval = i.score + A / math.sqrt(i.visits)
        if new_eval > best_eval:
            best_eval = new_eval
            best_child = i
    return best_child


if __name__ == '__main__':
    # sys.setrecursionlimit(5000)
    board = LionBoard.LionBoard()
    board.setBoard_start()
    # board.setBoard_Fen("e1g/1Cl/G11/1LE/")
    # board.setBoard_Fen("el1/1Cg/L2/2E/cE")
    board.printBoard()

    print("")
    print("MCTS")
    result_node = MCTS_Solver(board, True, 3)
    #result_node = MCTS_MR_Solver(board, True, 3, 2)
    #result_node = MCTS_MS_Solver(board, True, 3, 4, 2)
    result_node.move.printMove()
    #print("Result node Children Count:", len(result_node.children))
    print("Root node Children Count:", len(result_node.parent.children))
    print("Visits:", result_node.visits)
    print("Score:", result_node.score)
