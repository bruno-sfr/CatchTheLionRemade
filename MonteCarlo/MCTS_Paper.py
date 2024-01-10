import copy
import math
import random
import sys
import time

from MonteCarlo import MCTS_Node
from Game import LionBoard, Move
from AlphaBeta import AlphaBeta

def MCTS_Paper_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_Paper(root, whiteTurn)
    return secure_child(root)

def MCTS_Paper(N: MCTS_Node, whiteTurn: bool):
#Integer MCTSSolver(Node N){
    if N.state.isGameOver():
        #if N.whiteTurn:
        if whiteTurn:
            if N.state.hasWhiteWon():
                # player to move wins
                N.backpropagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                N.backpropagete_value(float('-inf'))
                return float('-inf')
        else:
            if N.state.hasBlackWon():
                # player to move wins
                N.backpropagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                N.backpropagete_value(float('-inf'))
                return float('-inf')
#    if (playerToMoveWins(N))
#        return INFINITY
#    else if (playerToMoveLoses(N))
#        return -INFINITY

    best_child = select_Paper(N)
    N.visits = N.visits + 1
#    bestChild = select(N)
#    N.visitCount++
    #if best_child is None:
    #    best_child = select_Paper(N)


    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            #R = -simulation(best_child, best_child.whiteTurn)
            R = -simulation(best_child, whiteTurn)
            best_child.visits = 1
            N.add_child(best_child)
            N.backpropagete_value(R)
            return R
        else:
            #R = -MCTS_Paper(best_child)
            R = -MCTS_Paper(best_child, whiteTurn)
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


def MCTS_MR_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int, depth: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_MR(root, whiteTurn, depth)
    return secure_child(root)


def MCTS_MR(N: MCTS_Node, whiteTurn: bool, depth: int):
#Integer MCTSSolver(Node N){
    if N.state.isGameOver():
        #if N.whiteTurn:
        if whiteTurn:
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

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    #if best_child.visits != 0:
    #    best_child = select_Paper(N)

    #print("best child score:", best_child.score, " visits:", best_child.visits)
    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            #print("Rollout")
            #R = -MiniMax_Rollout(best_child, best_child.whiteTurn, depth)
            R = -MiniMax_Rollout(best_child, whiteTurn, depth)
            best_child.visits = 1
            N.add_child(best_child)
            N.backpropagete_value(R)
            return R
        else:
            #R = -MCTS_MR(best_child, depth)
            R = -MCTS_MR(best_child, whiteTurn, depth)
    else:
        R = best_child.score

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


def select_Paper(N: MCTS_Node):
    move_list = N.state.allpossibleMoves_BigList(N.whiteTurn)
    """if len(N.children) == 0 and len(move_list) > 0:
        # node is leaf with possible moves
        for move in move_list:
            check_board = copy.deepcopy(N.state)
            check_board.makeMove(N.whiteTurn, move.getFrom(), move.getTo())
            if check_board.isGameOver():
                new_child = MCTS_Node.MCTS_Node(N, check_board, not N.whiteTurn, move)
                N.add_child(new_child)
                #if not N.whiteTurn:
                if N.whiteTurn:
                # childs player to move
                    if check_board.hasWhiteWon():
                        # the player is white and has won so propagate win
                        new_child.backpropagete_value(float('inf'))
                    else:
                        new_child.backpropagete_value(float('-inf'))
                else:
                    if check_board.hasBlackWon():
                        # the player is black and has won so propagate win
                        new_child.backpropagete_value(float('inf'))
                    else:
                        new_child.backpropagete_value(float('-inf'))
                return new_child"""
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
                #state = copy.deepcopy(N.state)
                state = LionBoard.LionBoard()
                state.setBoard(N.state)
                state.makeMove(N.whiteTurn, move.getFrom(), move.getTo())
                new_child = MCTS_Node.MCTS_Node(N, state, not N.whiteTurn, move)
                #N.add_child(new_child)
                #print("new child visits:", new_child.visits)
                return new_child
    elif len(N.children) > 0:
        best_child = N.children[0]
        for child in N.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        #if best_child is None:
        #    pass
        return best_child
    else:
        # no move possible, is terminal node
        #print("Terminal Node")
        return None


def simulation(node: MCTS_Node, player: bool):
    #state = copy.deepcopy(node.state)
    state = LionBoard.LionBoard()
    state.setBoard(node.state)
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
    #print(i)
    if player and state.hasWhiteWon():
        return 1
    elif not player and state.hasBlackWon():
        return 1
    return 0


def MiniMax_Rollout(node: MCTS_Node, player: bool, depth: int):
    #state = copy.deepcopy(node.state)
    state = LionBoard.LionBoard()
    state.setBoard(node.state)
    whiteTurn = copy.deepcopy(node.whiteTurn)
    #MAX_ITERATIONS = 25
    MAX_ITERATIONS = 50
    #MAX_ITERATIONS = 100
    i = 0
    #state.printBoard()
    while i < MAX_ITERATIONS and not state.isGameOver():
        # while not state.isGameOver():
        # state.makeRandomMove(whiteTurn)
        eval, moves = AlphaBeta.alpha_beta_simple(depth, state, whiteTurn)
        #eval, moves = AlphaBeta.alpha_beta_win_loss_simple(depth, state, whiteTurn)
        # check if there are moves
        if len(moves) > 0:
            state.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo())
            #state.printBoard()
            whiteTurn = not whiteTurn
            i = i + 1
        else:
            return 0
    #print(i)
    if player and state.hasWhiteWon():
        return 1
    elif not player and state.hasBlackWon():
        return 1
    return 0


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
    #result_node = MCTS_Paper_Run(board, True, 3)
    result_node = MCTS_MR_Run(board, True, 3, 1)
    result_node.move.printMove()
    #print("Result node Children Count:", len(result_node.children))
    #print("Root node Children Count:", len(result_node.parent.children))
    print("Root node Visits:", result_node.parent.visits)
    print("Visits:", result_node.visits)
    print("Score:", result_node.score)