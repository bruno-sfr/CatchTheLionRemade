import copy
import math
import random
import sys
import time

from MonteCarlo import MCTS_Node_Paper
from Game import LionBoard, Move
from AlphaBeta import AlphaBeta

"""def MCTS_Paper_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int):
    none_move = Move.Move()
    root = MCTS_Node_Paper.MCTS_Node_Paper(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_Paper(root)
    return secure_child(root)
    # return best_child(root)

def MCTS_Paper(N: MCTS_Node_Paper):
    if N.state.isGameOver():
        if N.whiteTurn:
            # it is whites Turn in Node
            if N.state.hasBlackWon():
                # Black has won, so white loses (this node)
                N.add_value(float('-inf'))
                return float('-inf')
            elif N.state.hasWhiteWon():
                # Black has lost, so white wins (this node)
                N.add_value(float('inf'))
                return float('inf')
            else:
                # draw
                return 0
        else:
            # it is blacks Turn in Node
            if N.state.hasWhiteWon():
                # White has won, so black loses (this node)
                N.add_value(float('-inf'))
                return float('-inf')
            elif N.state.hasBlackWon():
                # White has lost, so black wins (this node)
                N.add_value(float('inf'))
                return float('inf')
            else:
                # draw
                return 0

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child)
            best_child.add_value(-R)
            best_child.visits = best_child.visits + 1
            N.add_child(best_child)
            N.add_value(R)
            return R
        else:
            R = -MCTS_Paper(best_child)
    else:
        # Returns Proven Win or Loss
        R = best_child.score

    if R == float('inf'):
        N.score = float('-inf')
        return R
    elif R == float('-inf'):
        for child in N.children:
            if child.score != R:
                R = -1
                N.add_value(R)
                return R
        N.score = float('inf')
        return R
    else:
        N.add_value(R)
        return R"""

def MCTS_Paper_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int):
    none_move = Move.Move()
    root = MCTS_Node_Paper.MCTS_Node_Paper(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_Paper(root)
    return secure_child(root)
    # return best_child(root)

"""
Backup
def MCTS_Paper(N: MCTS_Node_Paper):
    if N.visits <= 1:
        #only usful on first call
        if playerToMoveWins(N):
            N.add_value(float('inf'))
            return float('inf')
        elif playerToMoveLoses(N):
            N.add_value(float('-inf'))
            return float('-inf')

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child)
            best_child.add_value(-R)
            best_child.visits = best_child.visits + 1
            N.add_child(best_child)
            N.add_value(R)
            return R
        else:
            R = -MCTS_Paper(best_child)
    else:
        # Returns Proven Win or Loss
        R = best_child.score


    if R == float('inf'):
        N.score = float('-inf')
        return R
    elif R == float('-inf'):
        for child in N.children:
            if child.score != R:
                R = -1
                N.add_value(R)
                return R
        N.score = float('inf')
        return R
    else:
        N.add_value(R)
        return R
"""

def MCTS_Paper(N: MCTS_Node_Paper):
    if N.visits <= 1:
        #only usful on first call
        if playerToMoveWins(N):
            N.add_value(float('inf'))
            return float('inf')
        elif playerToMoveLoses(N):
            N.add_value(float('-inf'))
            return float('-inf')

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child)
            best_child.add_value(-R)
            best_child.visits = best_child.visits + 1
            N.add_child(best_child)
            N.add_value(R)
            return R
        else:
            R = -MCTS_Paper(best_child)

            #double negation seems wrong
            #if R  == float('-inf') or R == float('inf'):
            #    R = -R
    else:
        # Returns Proven Win or Loss
        R = -best_child.score
        """invert score according to NegaMax Logic, or is that double negation?"""
        #R = -best_child.score


    if R == float('inf'):
        # child node has lost, so win for this node
        N.score = float('inf')
        return N.score
    elif R == float('-inf'):
        # child node has won, so that child produces loss for this node, how about the other children?
        for child in N.children:
            """also swap negation acording to negamax? also is double negation?"""
            if -child.score != R:
            #if child.score != -R:
                R = -1
                N.add_value(R)
                return R
        # all children produce loss for node, so node losses
        N.score = float('-inf')
        return N.score
    else:
        N.add_value(R)
        return R


def MCTS_Paper_MR_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int, depth:int):
    none_move = Move.Move()
    root = MCTS_Node_Paper.MCTS_Node_Paper(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_Paper_MR(root, depth)
    return secure_child(root)
    # return best_child(root)

def MCTS_Paper_MR(N: MCTS_Node_Paper, Depth:int):
    if N.visits <= 1:
        #only usful on first call
        if playerToMoveWins(N):
            N.add_value(float('inf'))
            return float('inf')
        elif playerToMoveLoses(N):
            N.add_value(float('-inf'))
            return float('-inf')

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -MiniMax_simulation(best_child, Depth)
            best_child.add_value(-R)
            best_child.visits = best_child.visits + 1
            N.add_child(best_child)
            N.add_value(R)
            return R
        else:
            R = -MCTS_Paper_MR(best_child, Depth)

            #double negation seems wrong
            #if R  == float('-inf') or R == float('inf'):
            #    R = -R
    else:
        # Returns Proven Win or Loss
        R = -best_child.score
        """invert score according to NegaMax Logic, or is that double negation?"""
        #R = -best_child.score


    if R == float('inf'):
        # child node has lost, so win for this node
        N.score = float('inf')
        return N.score
    elif R == float('-inf'):
        # child node has won, so that child produces loss for this node, how about the other children?
        for child in N.children:
            """also swap negation acording to negamax? also is double negation?"""
            if -child.score != R:
            #if child.score != -R:
                R = -1
                N.add_value(R)
                return R
        # all children produce loss for node, so node losses
        N.score = float('-inf')
        return N.score
    else:
        N.add_value(R)
        return R

def MCTS_Paper_MS_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int, threshold: int, depth: int):
    none_move = Move.Move()
    root = MCTS_Node_Paper.MCTS_Node_Paper(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_Paper_MS(root, threshold, depth)
    return secure_child(root)
    # return best_child(root)

def MCTS_Paper_MS(N: MCTS_Node_Paper, threshold: int, depth: int):
    if N.visits <= 1:
        #only usful on first call
        if playerToMoveWins(N):
            N.add_value(float('inf'))
            return float('inf')
        elif playerToMoveLoses(N):
            N.add_value(float('-inf'))
            return float('-inf')

    if N.visits == threshold and N.parent is not None:
        """for child in N.children:
            eval, move = AlphaBeta.alpha_beta_win_loss_simple(depth, child.state, child.whiteTurn)
            if child.whiteTurn:
                # child plays for white
                if eval == 1:
                    #child wins
                    child.add_value(float('inf'))
                    continue
                elif eval == -1:
                    #child losses, so win for node
                    child.add_value(float('-inf'))
                    N.score = float('inf')
                    return N.score
            else:
                # child plays for black
                if eval == -1:
                    #child wins
                    child.add_value(float('inf'))
                    continue
                elif eval == 1:
                    #child losses, so win for node
                    child.add_value(float('-inf'))
                    N.score = float('inf')
                    return N.score"""

        # visit threshold met, and node is not root
        eval, move = AlphaBeta.alpha_beta_win_loss_simple(depth, N.state, N.whiteTurn)
        if N.whiteTurn:
            # whites turn to move in Node
            if eval == 1:
                #white wins, so proven win for node
                N.add_value(float('inf'))
                return float('inf')
            elif eval == -1:
                #black wins, so proven loss for node
                N.add_value(float('-inf'))
                return float('-inf')
        else:
            # blacks turn to move in Node
            if eval == 1:
                # white wins, so proven loss for node
                N.add_value(float('-inf'))
                return float('-inf')
            elif eval == -1:
                # black wins, so proven win for node
                N.add_value(float('inf'))
                return float('inf')

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child)
            best_child.add_value(-R)
            best_child.visits = best_child.visits + 1
            N.add_child(best_child)
            N.add_value(R)
            return R
        else:
            R = -MCTS_Paper_MS(best_child, threshold, depth)

            #double negation seems wrong
            #if R  == float('-inf') or R == float('inf'):
            #    R = -R
    else:
        # Returns Proven Win or Loss
        R = -best_child.score
        """invert score according to NegaMax Logic, or is that double negation?"""
        #R = -best_child.score


    if R == float('inf'):
        # child node has lost, so win for this node
        N.score = float('inf')
        return N.score
    elif R == float('-inf'):
        # child node has won, so that child produces loss for this node, how about the other children?
        for child in N.children:
            """also swap negation acording to negamax? also is double negation?"""
            if -child.score != R:
            #if child.score != -R:
                R = -1
                N.add_value(R)
                return R
        # all children produce loss for node, so node losses
        N.score = float('-inf')
        return N.score
    else:
        N.add_value(R)
        return R

def MCTS_Paper_MB_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int, depth: int):
    none_move = Move.Move()
    root = MCTS_Node_Paper.MCTS_Node_Paper(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_Paper_MB(root, depth)
    return secure_child(root)

def MCTS_Paper_MB(N: MCTS_Node_Paper, depth: int):
    if N.visits <= 1:
        #only usful on first call
        if playerToMoveWins(N):
            N.add_value(float('inf'))
            return float('inf')
        elif playerToMoveLoses(N):
            N.add_value(float('-inf'))
            return float('-inf')

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child)
            best_child.add_value(-R)
            best_child.visits = best_child.visits + 1
            N.add_child(best_child)
            N.add_value(R)
            return R
        else:
            R = -MCTS_Paper_MB(best_child, depth)

            #double negation seems wrong
            #if R  == float('-inf') or R == float('inf'):
            #    R = -R
    else:
        # Returns Proven Win or Loss
        R = -best_child.score
        """invert score according to NegaMax Logic, or is that double negation?"""
        #R = -best_child.score


    if R == float('inf'):
        # child node has lost, so win for this node
        N.score = float('inf')
        return N.score
    elif R == float('-inf'):
        # child node has won, so that child produces loss for this node, how about the other children?
        for child in N.children:
            """also swap negation acording to negamax? also is double negation?"""
            if -child.score != R:
                eval, move = AlphaBeta.alpha_beta_win_loss_simple(depth, child.state, child.whiteTurn)
                if child.whiteTurn:
                    # child plays for white
                    if eval == 1:
                        #child wins
                        child.add_value(float('inf'))
                        continue
                    elif eval == -1:
                        #child losses, so win for node
                        child.add_value(float('-inf'))
                        N.score = float('inf')
                        return N.score
                    else:
                        R = -1
                        N.add_value(R)
                        return R
                else:
                    # child plays for black
                    if eval == -1:
                        #child wins
                        child.add_value(float('inf'))
                        continue
                    elif eval == 1:
                        #child losses, so win for node
                        child.add_value(float('-inf'))
                        N.score = float('inf')
                        return N.score
                    else:
                        R = -1
                        N.add_value(R)
                        return R
        # all children produce loss for node, so node losses
        N.score = float('-inf')
        return N.score
    else:
        N.add_value(R)
        return R

"""Not Finished
def Minimax_Selection(N: MCTS_Node_Paper, threshold: int, depth: int):
    moves = N.state.allpossibleMoves_BigList(N.whiteTurn)
    child_whiteTurn = not N.whiteTurn
    for move in moves:
        board = LionBoard.LionBoard()
        board.setBoard(N.state)
        board.makeMove(N.whiteTurn, move.getFrom(), move.getTo())
        eval, move = AlphaBeta.alpha_beta_win_loss_simple(depth, N.state, N.whiteTurn)
        if N.whiteTurn:
            # whites turn to move in Node
            if eval == 1:
                # white wins, so proven win for node
                N.add_value(float('inf'))
                return float('inf')
            elif eval == -1:
                # black wins, so proven loss for node
                N.add_value(float('-inf'))
                return float('-inf')
        else:
            # blacks turn to move in Node
            if eval == 1:
                # white wins, so proven loss for node
                N.add_value(float('-inf'))
                return float('-inf')
            elif eval == -1:
                # black wins, so proven win for node
                N.add_value(float('inf'))
                return float('inf')"""

"""def MCTS_Paper_MR(N: MCTS_Node_Paper, depth:int):
    #if N.state.isGameOver():
    #    if N.whiteTurn:
    #        FLIPPING THE MINUS AS A TEST AND COMMENTING OUT ADD VALUE
    #        # it is whites Turn in Node
    #        if N.state.hasBlackWon():
    #            # Black has won, so white loses (this node)
    #            N.add_value(float('-inf'))
    #            return float('-inf')
    #            #return float('inf')
    #        elif N.state.hasWhiteWon():
    #            # Black has lost, so white wins (this node)
    #            N.add_value(float('inf'))
    #            return float('inf')
    #            #return float('-inf')
    #        else:
    #            # draw
    #            return 0
    #    else:
    #        # it is blacks Turn in Node
    #        if N.state.hasWhiteWon():
    #            # White has won, so black loses (this node)
    #            N.add_value(float('-inf'))
    #            return float('-inf')
    #            #return float('inf')
    #        elif N.state.hasBlackWon():
    #            # White has lost, so black wins (this node)
    #            N.add_value(float('inf'))
    #            return float('inf')
    #            #return float('-inf')
    #        else:
    #            # draw
    #            return 0
    #if N.parent is not None:
    if playerToMoveWins(N):
        N.add_value(float('inf'))
        return float('inf')
    elif playerToMoveLoses(N):
        N.add_value(float('-inf'))
        return float('-inf')

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -MiniMax_simulation(best_child, depth)
            best_child.add_value(-R)
            best_child.visits = best_child.visits + 1
            N.add_child(best_child)
            N.add_value(R)
            return R
        else:
            R = -MCTS_Paper_MR(best_child, depth)
    else:
        # Returns Proven Win or Loss
        R = best_child.score

    if R == float('inf'):
        N.score = float('-inf')
        return R
    elif R == float('-inf'):
        for child in N.children:
            if child.score != R:
                R = -1
                N.add_value(R)
                return R
        N.score = float('inf')
        return R
    else:
        N.add_value(R)
        return R"""

"""def MCTS_Paper_MS(N: MCTS_Node_Paper, threshold: int, depth: int):
    if N.state.isGameOver():
        if N.whiteTurn:
            # it is whites Turn in Node
            if N.state.hasBlackWon():
                # Black has won, so white loses (this node)
                N.add_value(float('-inf'))
                return float('-inf')
            elif N.state.hasWhiteWon():
                # Black has lost, so white wins (this node)
                N.add_value(float('inf'))
                return float('inf')
            else:
                # draw
                return 0
        else:
            # it is blacks Turn in Node
            if N.state.hasWhiteWon():
                # White has won, so black loses (this node)
                N.add_value(float('-inf'))
                return float('-inf')
            elif N.state.hasBlackWon():
                # White has lost, so black wins (this node)
                N.add_value(float('inf'))
                return float('inf')
            else:
                # draw
                return 0

    #if N.visits == threshold:
    #    eval, move = AlphaBeta.alpha_beta_win_loss_simple(depth, N.state, N.whiteTurn)
    #    if N.whiteTurn:
    #        # it is whites Turn in Node
    #        if eval == 1:
    #            # White has won (this node)
    #            N.add_value(float('inf'))
     #           return float('inf')
    #        elif eval == -1:
    #            # White has lost(this node)
    #            N.add_value(float('-inf'))
    #            return float('-inf')
    #    else:
    #        # it is blacks Turn in Node
    #        if eval == -1:
    #            # black has won (this node)
    #            N.add_value(float('inf'))
     #           return float('inf')
     #       elif eval == -1:
     #           # black has lost(this node)
     #           N.add_value(float('-inf'))
     #           return float('-inf')

    best_child = select_Paper_MS(N, threshold, depth)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child)
            best_child.add_value(-R)
            best_child.visits = best_child.visits + 1
            N.add_child(best_child)
            N.add_value(R)
            return R
        else:
            R = -MCTS_Paper_MS(best_child, threshold, depth)
    else:
        # Returns Proven Win or Loss
        R = best_child.score

    if R == float('inf'):
        N.score = float('-inf')
        return R
    elif R == float('-inf'):
        for child in N.children:
            if child.score != R:
                R = -1
                N.add_value(R)
                return R
        N.score = float('inf')
        return R
    else:
        N.add_value(R)
        return R

def select_Paper_MS(N: MCTS_Node_Paper, threshold: int, depth: int):
    move_list = N.state.allpossibleMoves_BigList(N.whiteTurn)
    if len(N.children) < len(move_list):
        # Since Move list is bigger than the number of Childrens, there is a yet unexplored Child
        for move in move_list:
            move_in_children = False
            for child in N.children:
                if child.move.equals(move):
                    move_in_children = True
            if move_in_children:
                continue
            else:
                # add node with move
                state = LionBoard.LionBoard()
                state.setBoard(N.state)
                state.makeMove(N.whiteTurn, move.getFrom(), move.getTo())
                child_whiteTurn = not N.whiteTurn
                new_child = MCTS_Node_Paper.MCTS_Node_Paper(N, state, child_whiteTurn, move)
                return new_child
    #if N.visits >= threshold:
    #    eval, move = AlphaBeta.alpha_beta_win_loss_simple(depth, N.state, N.whiteTurn)
    #    if N.whiteTurn:
    #        # it is whites Turn in Node
    #        if eval == 1:
    #            # White has won (this node)
    #            N.add_value(float('inf'))
    #            return float('inf')
    #        elif eval == -1:
    #            # White has lost(this node)
    #            N.add_value(float('-inf'))
    #            return float('-inf')
    #    else:
    #        # it is blacks Turn in Node
    #        if eval == -1:
     #           # black has won (this node)
     #           N.add_value(float('inf'))
      #          return float('inf')
       #     elif eval == -1:
       #         # black has lost(this node)
       #         N.add_value(float('-inf'))
       #         return float('-inf')
    if N.visits >= threshold and len(N.children) > 0:
        for child in N.children:
            eval, move = AlphaBeta.alpha_beta_win_loss_simple(depth, child.state, child.whiteTurn)
            if child.whiteTurn:
                # it is whites Turn in Child
                if eval == 1:
                    # White has won (this child)
                    child.add_value(float('inf'))
                    return child
                elif eval == -1:
                    # White has lost(this child)
                    child.add_value(float('-inf'))
            else:
                # it is blacks Turn in Child
                if eval == -1:
                    # black has won (this child)
                    child.add_value(float('inf'))
                    return child
                elif eval == -1:
                    # black has lost(this child)
                    child.add_value(float('-inf'))
    if len(N.children) > 0:
        # UCT = self.score / self.visits + math.sqrt(C * math.log(parent.visits)/self.visits)
        best_child = N.children[0]
        best_UCT = N.children[0].UCT()
        for child in N.children:
            child_UCT = child.UCT()
            if best_UCT < child_UCT:
                best_child = child
                best_UCT = child_UCT
        return best_child
    else:
        # no move possible, is terminal node
        # print("Terminal Node")
        return None"""

"""def MCTS_Paper_MS_Run(state: LionBoard, whiteTurn: bool, timeout_seconds: int, threshhold: int, Depth: int):
    none_move = Move.Move()
    root = MCTS_Node_Paper.MCTS_Node_Paper(None, state, whiteTurn, none_move)
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        MCTS_Paper_MS(root, threshhold, Depth)
    return secure_child(root)
    # return best_child(root)

def MCTS_Paper_MS(N: MCTS_Node_Paper, threshhold: int, Depth: int):
    if N.visits <= 1:
        #only usful on first call
        if playerToMoveWins(N):
            N.add_value(float('inf'))
            return float('inf')
        elif playerToMoveLoses(N):
            N.add_value(float('-inf'))
            return float('-inf')

    if N.visits == threshhold:
        eval, move = AlphaBeta.alpha_beta_win_loss_simple(Depth, N.state, N.whiteTurn)
        if N.whiteTurn:
            # whites turn to move in Node
            if eval == 1:
                #white wins, so proven win for node
                N.add_value(float('inf'))
                return float('inf')
            elif eval == -1:
                #black wins, so proven loss for node
                N.add_value(float('-inf'))
                return float('-inf')
        else:
            # blacks turn to move in Node
            if eval == 1:
                # white wins, so proven loss for node
                N.add_value(float('-inf'))
                return float('-inf')
            elif eval == -1:
                # black wins, so proven win for node
                N.add_value(float('inf'))
                return float('inf')

    best_child = select_Paper(N)
    N.visits = N.visits + 1
    if best_child is None:
        # best_child = select_Paper(N)
        return 0

    if best_child.score != float('-inf') and best_child.score != float('inf'):
        if best_child.visits == 0:
            R = -simulation(best_child)
            best_child.add_value(-R)
            best_child.visits = best_child.visits + 1
            N.add_child(best_child)
            N.add_value(R)
            return R
        else:
            R = -MCTS_Paper_MS(best_child, threshhold, Depth)
    else:
        # Returns Proven Win or Loss
        R = best_child.score

    if R == float('inf'):
        N.score = float('-inf')
        return R
    elif R == float('-inf'):
        for child in N.children:
            if child.score != R:
                R = -1
                N.add_value(R)
                return R
        N.score = float('inf')
        return R
    else:
        N.add_value(R)
        return R"""


def select_Paper(N: MCTS_Node_Paper):
    move_list = N.state.allpossibleMoves_BigList(N.whiteTurn)
    if len(N.children) < len(move_list):
        # Since Move list is bigger than the number of Childrens, there is a yet unexplored Child
        for move in move_list:
            move_in_children = False
            for child in N.children:
                if child.move.equals(move):
                    move_in_children = True
            if move_in_children:
                continue
            else:
                # add node with move
                state = LionBoard.LionBoard()
                state.setBoard(N.state)
                state.makeMove(N.whiteTurn, move.getFrom(), move.getTo())
                child_whiteTurn = not N.whiteTurn
                new_child = MCTS_Node_Paper.MCTS_Node_Paper(N, state, child_whiteTurn, move)
                return new_child
    elif len(N.children) > 0:
        # UCT = self.score / self.visits + math.sqrt(C * math.log(parent.visits)/self.visits)
        best_child = N.children[0]
        best_UCT = N.children[0].UCT()
        for child in N.children:
            child_UCT = child.UCT()
            if best_UCT < child_UCT:
                best_child = child
                best_UCT = child_UCT
        return best_child
    else:
        # no move possible, is terminal node
        # print("Terminal Node")
        return None

def simulation(node: MCTS_Node_Paper):
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
            # count as Draw
            return 0
        whiteTurn = not whiteTurn
        i = i + 1
    #print(i)
    if not state.isGameOver():
        # time out, so draw
        return 0
    elif node.whiteTurn:
        # node plays for White
        if state.hasWhiteWon():
            # node has won
            return 1
        else:
            # node has lost
            return -1
    else:
        # node plays for White
        if state.hasBlackWon():
            # node has won
            return 1
        else:
            # node has lost
            return -1

def MiniMax_simulation(node: MCTS_Node_Paper, depth: int):
    #print("")
    #print("New MiniMax-Rollot")
    state = LionBoard.LionBoard()
    state.setBoard(node.state)
    #state.printBoard()
    #print("WhiteTurn:",node.whiteTurn)
    whiteTurn = copy.deepcopy(node.whiteTurn)
    MAX_ITERATIONS = 25
    i = 0
    while i < MAX_ITERATIONS and not state.isGameOver():
        # while not state.isGameOver():
        try:
            eval, move = AlphaBeta.alpha_beta_simple(depth, state, whiteTurn)
            #move.printMove()
            state.makeMove(whiteTurn, move.getFrom(), move.getTo())
        except Exception as e:
            print(e)
            # count as Draw
            return 0
        whiteTurn = not whiteTurn
        i = i + 1
    #print("End,move count:",i)
    if not state.isGameOver():
        # time out, so draw
        return 0
    elif node.whiteTurn:
        # node plays for White
        if state.hasWhiteWon():
            # node has won
            return 1
        else:
            # node has lost
            return -1
    else:
        # node plays for White
        if state.hasBlackWon():
            # node has won
            return 1
        else:
            # node has lost
            return -1

def playerToMoveWins(node: MCTS_Node_Paper):
    moves = node.state.allpossibleMoves_BigList(node.whiteTurn)
    for move in moves:
        board = LionBoard.LionBoard()
        board.setBoard(node.state)
        board.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
        if node.whiteTurn and board.hasWhiteWon():
            # node is white and has won
            return True
        elif not node.whiteTurn and board.hasBlackWon():
            # node is black and has won
            return True
    return False

def playerToMoveLoses(node: MCTS_Node_Paper):
    moves = node.state.allpossibleMoves_BigList(node.whiteTurn)
    PlayerLoses = True
    for move in moves:
        board = LionBoard.LionBoard()
        board.setBoard(node.state)
        board.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
        if not node.whiteTurn and board.hasWhiteWon():
            # node is black and white has won, so node loses
            #return True
            pass
        elif node.whiteTurn and board.hasBlackWon():
            # node is white and black has won, so node loses
            #return True
            pass
        else:
            # Move where he does not lose
            PlayerLoses = False
    return PlayerLoses

def secure_child(node: MCTS_Node_Paper):
    if playerToMoveWins(node):
        moves = node.state.allpossibleMoves_BigList(node.whiteTurn)
        for move in moves:
            board = LionBoard.LionBoard()
            board.setBoard(node.state)
            board.makeMove(node.whiteTurn, move.getFrom(), move.getTo())
            if node.whiteTurn and board.hasWhiteWon():
                # node is white and has won
                node.move = move
                return node
            elif not node.whiteTurn and board.hasBlackWon():
                # node is black and has won
                node.move = move
                return node


    A = 1
    best_child = node.children[0]
    #best_eval = (1 - (best_child.score/best_child.visits)) + A / math.sqrt(best_child.visits)
    best_eval = -best_child.score/best_child.visits + A / math.sqrt(best_child.visits)
    for i in node.children:
        """Big Test with Minus"""
        new_eval = -i.score/i.visits + A / math.sqrt(i.visits)
        #new_eval = (1 - (i.score / i.visits)) + A / math.sqrt(i.visits)
        if new_eval > best_eval:
            best_eval = new_eval
            best_child = i
    return best_child


if __name__ == '__main__':
    # sys.setrecursionlimit(5000)
    board = LionBoard.LionBoard()
    board.setBoard_start()
    # board.setBoard_Fen("e1g/1Cl/G11/1LE/")
    #board.setBoard_Fen("el1/1Cg/L2/2E/cE")

    #board.setBoard_Fen("eg1/lc1/1CL/G1E/")
    """best move is 3 to 6"""
    board.setBoard_Fen("eg1/1l1/GE1/1L1/cC")
    """Best Move is 5 to 8"""
    #board.makeMove(True, 1, 3)
    #board.makeMove(False, 10, 6)
    board.printBoard()
    times = []
    for i in range(100):
        #print("AB:")
        starttime = time.time()
        eval,move = AlphaBeta.alpha_beta_simple(5,board,True)
        endtime = time.time()
        #print("eval:", eval)
        times.append(endtime-starttime)
        #print("Time taken:", endtime-starttime)
    move.printMove()
    avg = 0
    for i in range(100):
        avg = avg + times[i]
    print("Avg. time =", avg/ len(times))
    #eval, moves = AlphaBeta.alpha_beta_allMoves_simple(5, board, True)
    #print("eval:", eval)
    #for move in moves:
    #    move.printMove()

    """print("MCTS:")
    #result_node = MCTS_Paper_Run(board, True, 2)
    #result_node = MCTS_Paper_MS_Run(board, True, 2, 2,4)
    result_node = MCTS_Paper_MR_Run(board, True, 2, 2)
    #result_node = MCTS_Paper_MB_Run(board, True, 1, 4)
    Root = result_node.parent
    #for i in range(len(Root.children)):
    #    print("Child",i, "value:", Root.children[i].score)
        #child.state.printBoard()
    result_node.move.printMove()
    # print("Result node Children Count:", len(result_node.children))
    # print("Root node Children Count:", len(result_node.parent.children))
    print("Root node Visits:", result_node.parent.visits)
    print("Visits:", result_node.visits)
    print("Score:", -result_node.score)"""
