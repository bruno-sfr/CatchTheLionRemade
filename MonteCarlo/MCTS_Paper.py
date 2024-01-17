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
    # return best_child(root)


# Integer MCTSSolver(Node N){
#    if (playerToMoveWins(N))
#        return INFINITY
#    else if (playerToMoveLoses(N))
#        return -INFINITY

#    bestChild = select(N)
#    N.visitCount++

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

# DONE:
#    N.computeAverage(R)
#    return R
# }

def MCTS_Paper(N: MCTS_Node, whiteTurn: bool):
    if N.state.isGameOver():
        #if N.whiteTurn:
        if whiteTurn:
            if N.state.hasWhiteWon():
                # player to move wins
                # N.propagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                # N.propagete_value(float('-inf'))
                return float('-inf')
        else:
            if N.state.hasBlackWon():
                # player to move wins
                # N.propagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                # N.propagete_value(float('-inf'))
                return float('-inf')

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child, best_child.whiteTurn)
            #R = -simulation(best_child, whiteTurn)
            # print(R)
            best_child.visits = 1
            N.add_child(best_child)
            N.propagete_value(R)
            return R
        else:
            # R = -MCTS_Paper(best_child)
            R = -MCTS_Paper(best_child, whiteTurn)
    else:
        R = best_child.score

    if R == float('inf'):
        N.score = float('-inf')
        return R
    elif R == float('-inf'):
        for child in N.children:
            if child.score != R:
                R = -1
                N.propagete_value(R)
                return R
        N.score = float('inf')
        return R
    else:
        N.propagete_value(R)
        return R


def MCTS_MR_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int, depth: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_MR(root, whiteTurn, depth)
    return secure_child(root)
    # return best_child(root)


def MCTS_MR(N: MCTS_Node, whiteTurn: bool, depth: int):
    if N.state.isGameOver():
        #if N.whiteTurn:
        if whiteTurn:
            if N.state.hasWhiteWon():
                # player to move wins
                # N.propagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                # N.propagete_value(float('-inf'))
                return float('-inf')
        else:
            if N.state.hasBlackWon():
                # player to move wins
                # N.propagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                # N.propagete_value(float('-inf'))
                return float('-inf')

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            #R = -MiniMax_Rollout(best_child, whiteTurn, depth)
            R = -MiniMax_Rollout(best_child, best_child.whiteTurn, depth)
            # print(R)
            best_child.visits = 1
            N.add_child(best_child)
            N.propagete_value(R)
            return R
        else:
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
                N.propagete_value(R)
                return R
        N.score = float('inf')
        return R
    else:
        N.propagete_value(R)
        return R


"""def MCTS_MR(N: MCTS_Node, whiteTurn: bool, depth: int):
#Integer MCTSSolver(Node N){
    if N.state.isGameOver():
        #if N.whiteTurn:
        if whiteTurn:
            if N.state.hasWhiteWon():
                # player to move wins
                #N.propagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                #N.propagete_value(float('-inf'))
                return float('-inf')
        else:
            if N.state.hasBlackWon():
                # player to move wins
                #N.propagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                #N.propagete_value(float('-inf'))
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
            #print(R)
            best_child.visits = 1
            N.add_child(best_child)
            N.propagete_value(R)
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
                N.propagete_value(R)
                return R
        N.score = float('inf')
        return R
    else:
        N.propagete_value(R)
        return R"""


def MCTS_MB_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int, depth: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_MB(root, whiteTurn, depth)
    return secure_child(root)


def MCTS_MB(N: MCTS_Node, whiteTurn: bool, depth: int):
    if N.state.isGameOver():
        # if N.whiteTurn:
        if whiteTurn:
            if N.state.hasWhiteWon():
                # player to move wins
                # N.propagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                # N.propagete_value(float('-inf'))
                return float('-inf')
        else:
            if N.state.hasBlackWon():
                # player to move wins
                # N.propagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                # N.propagete_value(float('-inf'))
                return float('-inf')

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        #best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child, best_child.whiteTurn)
            # R = -simulation(best_child, whiteTurn)
            # print(R)
            best_child.visits = 1
            N.add_child(best_child)
            N.propagete_value(R)
            return R
        else:
            # R = -MCTS_Paper(best_child)
            R = -MCTS_MB(best_child, whiteTurn, depth)
    else:
        R = best_child.score

    if R == float('inf'):
        N.score = float('-inf')
        return R
    elif R == float('-inf'):
        for child in N.children:
            if child.score != R:
                # MiniMax - Backpropagation
                eval, move = AlphaBeta.alpha_beta_win_loss_simple(depth, child.state, child.whiteTurn)
                #print("Eval:", eval, " Child WhiteTurn:", child.whiteTurn)
                if eval == -1:
                    # loss for opponent
                    continue
                else:
                    R = -1
                    N.propagete_value(R)
                    return R
        N.score = float('inf')
        return R
    else:
        N.propagete_value(R)
        return R


def MCTS_MS_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int, threshold: int, depth: int):
    none_move = Move.Move()
    root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_MS(root, whiteTurn, threshold, depth)
    return secure_child(root)


def MCTS_MS(N: MCTS_Node, whiteTurn: bool, threshold: int, depth: int):
    if N.state.isGameOver():
        if N.whiteTurn:
        #if whiteTurn:
            if N.state.hasWhiteWon():
                # player to move wins
                # N.propagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                # N.propagete_value(float('-inf'))
                return float('-inf')
        else:
            if N.state.hasBlackWon():
                # player to move wins
                # N.propagete_value(float('inf'))
                return float('inf')
            else:
                # player to move losses
                # N.propagete_value(float('-inf'))
                return float('-inf')

        """if N.visits == threshold:
        eval, move = AlphaBeta.alpha_beta_win_loss_simple(depth, N.state, N.whiteTurn)
        if N.whiteTurn:
        #if whiteTurn:
            if eval == 1:
                # win
                print("MS used")
                #N.propagete_value(float('inf'))
                N.visits = N.visits + 1
                return float('inf')
            elif eval == -1:
                # Loss
                print("MS used")
                #N.propagete_value(float('-inf'))
                N.visits = N.visits + 1
                return float('-inf')
        else:
            if eval == -1:
                # win
                print("MS used")
                #N.propagete_value(float('inf'))
                N.visits = N.visits + 1
                return float('inf')
            elif eval == 1:
                # Loss
                print("MS used")
                #N.propagete_value(float('-inf'))
                N.visits = N.visits + 1
                return float('-inf')"""
        """if eval == 1:
            # Node win
            print("MS used")
            #N.propagete_value(float('inf'))
            N.visits = N.visits + 1
            return float('inf')
        elif eval == -1:
            # Node Loss
            print("MS used")
            #N.propagete_value(float('-inf'))
            N.visits = N.visits + 1
            return float('-inf')"""

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        best_child = select_Paper(N)

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child, best_child.whiteTurn)
            # R = -simulation(best_child, whiteTurn)
            # print(R)
            best_child.visits = 1
            N.add_child(best_child)
            N.propagete_value(R)
            return R
        else:
            # R = -MCTS_Paper(best_child)
            R = -MCTS_MS(best_child, whiteTurn, threshold, depth)
    else:
        R = best_child.score

    if R == float('inf'):
        N.score = float('-inf')
        return R
    elif R == float('-inf'):
        for child in N.children:
            if child.score != R:
                R = -1
                N.propagete_value(R)
                return R
        N.score = float('inf')
        return R
    else:
        N.propagete_value(R)
        return R


"""def select_MS(N: MCTS_Node, whiteTurn: bool, threshold: int, depth: int):
    if N.visits >= threshold:
        #print("Run MS")
        eval, move = AlphaBeta.alpha_beta_win_loss_simple(depth, N.state, whiteTurn)
        if (eval == 1 and whiteTurn) or (eval == -1 and not whiteTurn):
            # win
            R = float('inf')
            N.propagete_value(R)
            return N
        if (eval == -1 and whiteTurn) or (eval == 1 and not whiteTurn):
            # loss
            R = float('-inf')
            N.propagete_value(R)
            return N

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
                # state = copy.deepcopy(N.state)
                state = LionBoard.LionBoard()
                state.setBoard(N.state)
                state.makeMove(N.whiteTurn, move.getFrom(), move.getTo())
                new_child = MCTS_Node.MCTS_Node(N, state, not N.whiteTurn, move)
                # N.add_child(new_child)
                # print("new child visits:", new_child.visits)
                return new_child
    elif len(N.children) > 0:
        best_child = N.children[0]
        for child in N.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        # if best_child is None:
        #    pass
        return best_child
    else:
        # no move possible, is terminal node
        # print("Terminal Node")
        return None"""


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
                # state = copy.deepcopy(N.state)
                state = LionBoard.LionBoard()
                state.setBoard(N.state)
                state.makeMove(N.whiteTurn, move.getFrom(), move.getTo())
                new_child = MCTS_Node.MCTS_Node(N, state, not N.whiteTurn, move)
                # N.add_child(new_child)
                # print("new child visits:", new_child.visits)
                return new_child
    elif len(N.children) > 0:
        best_child = N.children[0]
        for child in N.children:
            if best_child.UCT() < child.UCT():
                best_child = child
        # if best_child is None:
        #    pass
        return best_child
    else:
        # no move possible, is terminal node
        # print("Terminal Node")
        return None


def simulation(node: MCTS_Node, player: bool):
    # state = copy.deepcopy(node.state)
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
                # return 0
                return -1
            else:
                return 1
        whiteTurn = not whiteTurn
        i = i + 1
    # print(i)
    if player and state.hasWhiteWon():
        # print(1)
        return 1
    elif player and state.hasBlackWon():
        # print(-1)
        return -1
    elif not player and state.hasBlackWon():
        # print(1)
        return 1
    elif not player and state.hasWhiteWon():
        # print(-1)
        return -1
    # print(0)
    return 0


def MiniMax_Rollout(node: MCTS_Node, player: bool, depth: int):
    # state = copy.deepcopy(node.state)
    state = LionBoard.LionBoard()
    state.setBoard(node.state)
    whiteTurn = copy.deepcopy(node.whiteTurn)
    MAX_ITERATIONS = 10
    # MAX_ITERATIONS = 25
    # MAX_ITERATIONS = 50
    # MAX_ITERATIONS = 100
    i = 0
    while i < MAX_ITERATIONS and not state.isGameOver():
        # while not state.isGameOver():
        # state.makeRandomMove(whiteTurn)
        eval, move = AlphaBeta.alpha_beta_simple(depth, state, whiteTurn)
        # eval, moves = AlphaBeta.alpha_beta_win_loss_simple(depth, state, whiteTurn)
        # check if there are moves
        if move is not None:
            state.makeMove(whiteTurn, move.getFrom(), move.getTo())
            # state.printBoard()
            whiteTurn = not whiteTurn
            i = i + 1
        else:
            if player == whiteTurn:
                # return 0
                return -1
            else:
                return 1
    # print(i)
    if player and state.hasWhiteWon():
        # print(1)
        return 1
    elif player and state.hasBlackWon():
        # print(-1)
        return -1
    elif not player and state.hasBlackWon():
        # print(1)
        return 1
    elif not player and state.hasWhiteWon():
        # print(-1)
        return -1
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


def best_child(node: MCTS_Node):
    best_child = node.children[0]
    for i in node.children:
        if i.visits > best_child.visits:
            best_child = i
    return best_child

class MCTS:
    def __init__(self):
        self.AB = AlphaBeta.Alpha_Beta_TT_Final()

    def MCTS_MR_TT_Run(self, state: LionBoard, whiteTurn: bool, timeout_seconds: int, depth: int):
        none_move = Move.Move()
        root = MCTS_Node.MCTS_Node(None, state, whiteTurn, none_move)
        start_time = time.time()

        while time.time() - start_time < timeout_seconds:
            self.MCTS_MR_TT(root, whiteTurn, depth)
        return secure_child(root)
        # return best_child(root)

    def MCTS_MR_TT(self, N: MCTS_Node, whiteTurn: bool, depth: int):
        if N.state.isGameOver():
            # if N.whiteTurn:
            if whiteTurn:
                if N.state.hasWhiteWon():
                    # player to move wins
                    # N.propagete_value(float('inf'))
                    return float('inf')
                else:
                    # player to move losses
                    # N.propagete_value(float('-inf'))
                    return float('-inf')
            else:
                if N.state.hasBlackWon():
                    # player to move wins
                    # N.propagete_value(float('inf'))
                    return float('inf')
                else:
                    # player to move losses
                    # N.propagete_value(float('-inf'))
                    return float('-inf')

        best_child = select_Paper(N)
        N.visits = N.visits + 1
        if best_child is None:
            # best_child = select_Paper(N)
            return 0

        if best_child.score != float('-inf') and best_child.score != float('inf'):
            if best_child.visits == 0:
                # R = -MiniMax_Rollout(best_child, whiteTurn, depth)
                R = -self.MiniMax_Rollout_TT(best_child, best_child.whiteTurn, depth)
                # print(R)
                best_child.visits = 1
                N.add_child(best_child)
                N.propagete_value(R)
                return R
            else:
                R = -self.MCTS_MR_TT(best_child, whiteTurn, depth)
        else:
            R = best_child.score

        if R == float('inf'):
            N.score = float('-inf')
            return R
        elif R == float('-inf'):
            for child in N.children:
                if child.score != R:
                    R = -1
                    N.propagete_value(R)
                    return R
            N.score = float('inf')
            return R
        else:
            N.propagete_value(R)
            return R

    def MiniMax_Rollout_TT(self, node: MCTS_Node, player: bool, depth: int):
        # state = copy.deepcopy(node.state)
        state = LionBoard.LionBoard()
        state.setBoard(node.state)
        whiteTurn = copy.deepcopy(node.whiteTurn)
        MAX_ITERATIONS = 10
        # MAX_ITERATIONS = 25
        # MAX_ITERATIONS = 50
        # MAX_ITERATIONS = 100
        i = 0
        while i < MAX_ITERATIONS and not state.isGameOver():
            eval, move = self.AB.alpha_beta_TT_final_simple(depth, state, whiteTurn)
            if move is not None:
                state.makeMove(whiteTurn, move.getFrom(), move.getTo())
                # state.printBoard()
                whiteTurn = not whiteTurn
                i = i + 1
            else:
                if player == whiteTurn:
                    return -1
                else:
                    return 1
        if player and state.hasWhiteWon():
            return 1
        elif player and state.hasBlackWon():
            return -1
        elif not player and state.hasBlackWon():
            return 1
        elif not player and state.hasWhiteWon():
            return -1
        return 0


if __name__ == '__main__':
    # sys.setrecursionlimit(5000)
    board = LionBoard.LionBoard()
    board.setBoard_start()
    # board.setBoard_Fen("e1g/1Cl/G11/1LE/")
    # board.setBoard_Fen("el1/1Cg/L2/2E/cE")
    # board.makeMove(True, 4, 7)
    board.printBoard()

    print("")
    print("MCTS")

    #result_node = MCTS_Paper_Run(board, True, 1)
    #result_node = MCTS_MR_Run(board, True, 1, 1)
    #result_node = MCTS_MB_Run(board, True, 3, 4)
    result_node = MCTS_MS_Run(board, True, 1, 2, 4)
    result_node.move.printMove()
    # print("Result node Children Count:", len(result_node.children))
    # print("Root node Children Count:", len(result_node.parent.children))
    print("Root node Visits:", result_node.parent.visits)
    print("Visits:", result_node.visits)
    print("Score:", result_node.score)
