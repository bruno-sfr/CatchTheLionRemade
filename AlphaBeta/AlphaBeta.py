import copy
import random
import time

from Game import LionBoard, Zobrist, Move
from . import TranspostionTable_Final
from . import HashEntry_Final
#import HashEntry_Flag
from . import AB_Flag
#import AB_Flag

"""
Algorithm from https://askeplaat.wordpress.com/534-2/mtdf-algorithm/
"""

class MTDF:
    def __init__(self):
        self.zob = Zobrist.Zobrist()
        self.AB = Alpha_Beta_TT()

    def MTDF(self, f: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool, increment):
        #increment = 0.1
        g = f
        #moves = []
        move = None
        upperbound = float('inf')
        lowerbound = float('-inf')
        while not (lowerbound >= upperbound):
            beta = 0.0
            if g == lowerbound:
                beta = g + increment
            else:
                beta = g

            g, move = self.AB.alpha_beta_TT(beta - increment, beta, depth, board, whiteTurn)

            if g < beta:
                upperbound = g
            else:
                lowerbound = g

        return g, move

    def MTDF_advanced(self, f: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool, increment):
        #increment = 0.1
        g = f
        #moves = []
        move = None
        upperbound = float('inf')
        lowerbound = float('-inf')
        while not (lowerbound >= upperbound):
            beta = 0.0
            if g == lowerbound:
                beta = g + increment
            else:
                beta = g

            g, move = self.AB.alpha_beta_advanced_TT(beta - increment, beta, depth, board, whiteTurn)

            if g < beta:
                upperbound = g
            else:
                lowerbound = g

        return g, move

class Alpha_Beta_TT:
    def __init__(self):
        self.zob = Zobrist.Zobrist()
        self.table = TranspostionTable_Final.TranspostionTable(20)

    def alpha_beta_advanced_TT(self, alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
        """
        :param alpha: best of max player
        :param beta:  best of min player
        :param depth: depth left
        :param board: game state
        :param whiteTurn: white is max player, black min player
        :param moves: list of move that lead to this game state
        :return: eval, list of moves
        """
        boardhash = self.zob.generateHash(board, whiteTurn)
        #boardFen = board.getFen()
        entry = self.table.probeEntry(boardhash)
        if entry != None:
            # check if hash matches
            if entry.Hash == boardhash:
                if entry.Depth == depth:
                    if entry.Flag == AB_Flag.Flag.EXACT:
                        return entry.Eval, entry.Move
                    elif entry.Flag == AB_Flag.Flag.LOWERBOUND:
                        # Update alpha with the lower bound
                        if entry.Eval >= beta:
                            return entry.Eval, entry.Move
                        alpha = max(alpha, entry.Eval)
                    elif entry.Flag == AB_Flag.Flag.UPPERBOUND:
                        # Update beta with the upper bound
                        if entry.Eval <= alpha:
                            return entry.Eval, entry.Move
                        beta = min(beta, entry.Eval)

        if depth == 0:
            eval = board.advanced_eval_func()
            #newEntry = HashEntry_Final.HashEntry(boardhash, depth, eval, AB_Flag.Flag.EXACT, Move.Move())
            #self.table.storeEntry(newEntry)
            return eval, None

        # if eval > 900 or eval < -900:
        if board.isGameOver():
            eval = board.advanced_eval_func()
            return eval, None

        if whiteTurn:
            maxEval = float('-inf')
            a = alpha
            bestmove = Move.Move()
            list = board.allpossibleMoves(whiteTurn)
            for i in list:
                for move in i:
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    new_whiteTurn = not whiteTurn
                    eval, Temp_Move = self.alpha_beta_advanced_TT(a, beta, depth - 1, new_board, new_whiteTurn)
                    if eval > maxEval:
                        maxEval = eval
                        bestmove = move
                    elif eval == maxEval:
                        rand = random.randint(0, 1)
                        if rand == 1:
                            bestmove = move
                    a = max(a, eval)
                    if not (maxEval < beta):
                        break
                else:
                    continue
                break

            if maxEval <= alpha:
                # Alpha Cutoff
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, maxEval, AB_Flag.Flag.UPPERBOUND, bestmove)
                self.table.storeEntry(newEntry)
            elif alpha < maxEval < beta:
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, maxEval, AB_Flag.Flag.EXACT, bestmove)
                self.table.storeEntry(newEntry)
            elif maxEval >= beta:
                # Beta Cutoff
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, maxEval, AB_Flag.Flag.LOWERBOUND, bestmove)
                self.table.storeEntry(newEntry)
            return maxEval, bestmove
        else:
            minEval = float('inf')
            b = beta
            bestmove = Move.Move()
            list = board.allpossibleMoves(whiteTurn)
            for i in list:
                for move in i:
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    new_whiteTurn = not whiteTurn
                    eval, Temp_Move = self.alpha_beta_advanced_TT(alpha, b, depth - 1, new_board, new_whiteTurn)
                    if eval < minEval:
                        minEval = eval
                        bestmove = move
                    elif eval == minEval:
                        rand = random.randint(0, 1)
                        if rand == 1:
                            bestmove = move
                    b = min(b, eval)
                    if not (minEval > alpha):
                        break
                else:
                    continue
                break

            if minEval <= alpha:
                # Alpha Cutoff
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, minEval, AB_Flag.Flag.UPPERBOUND, bestmove)
                self.table.storeEntry(newEntry)
            elif alpha < minEval < beta:
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, minEval, AB_Flag.Flag.EXACT, bestmove)
                self.table.storeEntry(newEntry)
            elif minEval >= beta:
                # Beta Cutoff
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, minEval, AB_Flag.Flag.LOWERBOUND, bestmove)
                self.table.storeEntry(newEntry)
            return minEval, bestmove

    def alpha_beta_advanced_TT_simple(self, depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
        eval, move = self.alpha_beta_advanced_TT(float('-inf'), float('inf'), depth, board, whiteTurn)
        return eval, move

    def alpha_beta_TT(self, alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
        """
        :param alpha: best of max player
        :param beta:  best of min player
        :param depth: depth left
        :param board: game state
        :param whiteTurn: white is max player, black min player
        :param moves: list of move that lead to this game state
        :return: eval, list of moves
        """
        boardhash = self.zob.generateHash(board, whiteTurn)
        #boardFen = board.getFen()
        entry = self.table.probeEntry(boardhash)
        if entry != None:
            # check if hash matches
            if entry.Hash == boardhash:
                if entry.Depth == depth:
                    if entry.Flag == AB_Flag.Flag.EXACT:
                        return entry.Eval, entry.Move
                    elif entry.Flag == AB_Flag.Flag.LOWERBOUND:
                        # Update alpha with the lower bound
                        if entry.Eval >= beta:
                            return entry.Eval, entry.Move
                        alpha = max(alpha, entry.Eval)
                    elif entry.Flag == AB_Flag.Flag.UPPERBOUND:
                        # Update beta with the upper bound
                        if entry.Eval <= alpha:
                            return entry.Eval, entry.Move
                        beta = min(beta, entry.Eval)

        if depth == 0:
            eval = board.eval_func()
            #newEntry = HashEntry_Final.HashEntry(boardhash, depth, eval, AB_Flag.Flag.EXACT, Move.Move())
            #self.table.storeEntry(newEntry)
            return eval, None

        # if eval > 900 or eval < -900:
        if board.isGameOver():
            eval = board.eval_func()
            return eval, None

        if whiteTurn:
            maxEval = float('-inf')
            a = alpha
            bestmove = Move.Move()
            list = board.allpossibleMoves(whiteTurn)
            for i in list:
                for move in i:
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    new_whiteTurn = not whiteTurn
                    eval, Temp_Move = self.alpha_beta_TT(a, beta, depth - 1, new_board, new_whiteTurn)
                    if eval > maxEval:
                        maxEval = eval
                        bestmove = move
                    a = max(a, eval)
                    if not (maxEval < beta):
                        break
                else:
                    continue
                break

            if maxEval <= alpha:
                # Alpha Cutoff
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, maxEval, AB_Flag.Flag.UPPERBOUND, bestmove)
                self.table.storeEntry(newEntry)
            elif alpha < maxEval < beta:
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, maxEval, AB_Flag.Flag.EXACT, bestmove)
                self.table.storeEntry(newEntry)
            elif maxEval >= beta:
                # Beta Cutoff
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, maxEval, AB_Flag.Flag.LOWERBOUND, bestmove)
                self.table.storeEntry(newEntry)
            return maxEval, bestmove
        else:
            minEval = float('inf')
            b = beta
            bestmove = Move.Move()
            list = board.allpossibleMoves(whiteTurn)
            for i in list:
                for move in i:
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    new_whiteTurn = not whiteTurn
                    eval, Temp_Move = self.alpha_beta_TT(alpha, b, depth - 1, new_board, new_whiteTurn)
                    if eval < minEval:
                        minEval = eval
                        bestmove = move
                    b = min(b, eval)
                    if not (minEval > alpha):
                        break
                else:
                    continue
                break

            if minEval <= alpha:
                # Alpha Cutoff
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, minEval, AB_Flag.Flag.UPPERBOUND, bestmove)
                self.table.storeEntry(newEntry)
            elif alpha < minEval < beta:
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, minEval, AB_Flag.Flag.EXACT, bestmove)
                self.table.storeEntry(newEntry)
            elif minEval >= beta:
                # Beta Cutoff
                newEntry = HashEntry_Final.HashEntry(boardhash, depth, minEval, AB_Flag.Flag.LOWERBOUND, bestmove)
                self.table.storeEntry(newEntry)
            return minEval, bestmove

    def alpha_beta_TT_simple(self, depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
        eval, move = self.alpha_beta_TT(float('-inf'), float('inf'), depth, board, whiteTurn)
        return eval, move

def alpha_beta_allMoves(alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool, moves: list):
    """
    :param alpha: best of max player
    :param beta:  best of min player
    :param depth: depth left
    :param board: game state
    :param whiteTurn: white is max player, black min player
    :param moves: list of move that lead to this game state
    :return: eval, list of moves
    """
    evals = []
    eval = board.eval_baier_func()

    if depth == 0:
        return eval, moves, [eval]

    if board.isGameOver():
        return eval, moves, [eval]

    best_moves = copy.deepcopy(moves)
    board_fen = board.getFen()

    if whiteTurn:
        maxEval = float('-inf')
        #list = board.allpossibleMoves(whiteTurn)
        list = board.allpossibleMoves_baier_capture(whiteTurn)
        for i in list:
            # print(len(i))
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_moves = copy.deepcopy(moves)
                new_moves.append(move)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, move_list, temp = alpha_beta_allMoves(alpha, beta, depth - 1, new_board, new_white_turn, new_moves)
                evals.append(eval)
                if eval > maxEval:
                    maxEval = eval
                    best_moves = move_list
                alpha = max(alpha, eval)
                if beta <= alpha:
                    return maxEval, best_moves, evals
        return maxEval, best_moves, evals
    else:
        minEval = float('inf')
        #list = board.allpossibleMoves(whiteTurn)
        list = board.allpossibleMoves_baier_capture(whiteTurn)
        for i in list:
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_moves = copy.deepcopy(moves)
                new_moves.append(move)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, move_list, temp = alpha_beta_allMoves(alpha, beta, depth - 1, new_board, new_white_turn, new_moves)
                evals.append(eval)
                if eval < minEval:
                    minEval = eval
                    best_moves = move_list
                beta = min(beta, eval)
                if beta <= alpha:
                    return minEval, best_moves, evals
        return minEval, best_moves, evals


def alpha_beta_allMoves_simple(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    eval, moves, evals = alpha_beta_allMoves(float('-inf'), float('inf'), depth, board, whiteTurn, [])
    return eval, moves, evals


def alpha_beta(alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    """
    :param alpha: best of max player
    :param beta:  best of min player
    :param depth: depth left
    :param board: game state
    :param whiteTurn: white is max player, black min player
    :param moves: list of move that lead to this game state
    :return: eval, list of moves
    """
    #eval = board.eval_func()
    eval = board.eval_baier_func()

    if depth == 0:
        return eval, None

    if board.isGameOver():
        return eval, None

    if whiteTurn:
        maxEval = float('-inf')
        bestmove = Move.Move()
        #list = board.allpossibleMoves(whiteTurn)
        list = board.allpossibleMoves_baier_capture(whiteTurn)
        for i in list:
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, Temp_Move = alpha_beta(alpha, beta, depth - 1, new_board, new_white_turn)
                if eval > maxEval:
                    maxEval = eval
                    bestmove = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    return maxEval, bestmove
        return maxEval, bestmove
    else:
        minEval = float('inf')
        bestmove = Move.Move()
        # list = board.allpossibleMoves(whiteTurn)
        list = board.allpossibleMoves_baier_capture(whiteTurn)
        for i in list:
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, Temp_Move = alpha_beta(alpha, beta, depth - 1, new_board, new_white_turn)
                if eval < minEval:
                    minEval = eval
                    bestmove = move
                beta = min(beta, eval)
                if beta <= alpha:
                    return minEval, bestmove
        return minEval, bestmove


def alpha_beta_simple(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    eval, move = alpha_beta(float('-inf'), float('inf'), depth, board, whiteTurn)
    return eval, move

def alpha_beta_advanced(alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    """
    :param alpha: best of max player
    :param beta:  best of min player
    :param depth: depth left
    :param board: game state
    :param whiteTurn: white is max player, black min player
    :param moves: list of move that lead to this game state
    :return: eval, list of moves
    """

    if depth == 0:
        eval = board.advanced_eval_func()
        return eval, None

    if board.isGameOver():
        eval = board.advanced_eval_func()
        return eval, None

    if whiteTurn:
        maxEval = float('-inf')
        bestmove = Move.Move()
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, Temp_Move = alpha_beta_advanced(alpha, beta, depth - 1, new_board, new_white_turn)
                if eval > maxEval:
                    maxEval = eval
                    bestmove = move
                #elif eval == maxEval:
                #    rand = random.randint(0, 1)
                #    if rand == 1:
                #        bestmove = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    return maxEval, bestmove
        return maxEval, bestmove
    else:
        minEval = float('inf')
        bestmove = Move.Move()
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, Temp_Move = alpha_beta_advanced(alpha, beta, depth - 1, new_board, new_white_turn)
                if eval < minEval:
                    minEval = eval
                    bestmove = move
                #elif eval == minEval:
                #    rand = random.randint(0, 1)
                #    if rand == 1:
                #        bestmove = move
                beta = min(beta, eval)
                if beta <= alpha:
                    return minEval, bestmove
        return minEval, bestmove


def alpha_beta_advanced_simple(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    eval, move = alpha_beta_advanced(float('-inf'), float('inf'), depth, board, whiteTurn)
    return eval, move

"""int Quiesce( int alpha, int beta ) {
    int stand_pat = Evaluate();
    if( stand_pat >= beta )
        return beta;
    if( alpha < stand_pat )
        alpha = stand_pat;

    until( every_capture_has_been_examined )  {
        MakeCapture();
        score = -Quiesce( -beta, -alpha );
        TakeBackMove();

        if( score >= beta )
            return beta;
        if( score > alpha )
           alpha = score;
    }
    return alpha;
}"""

#from gpt and ChessProgramming Wiki
def quiescence_search(alpha, beta, board, whiteTurn):
    #CPW
    """stand_pat = board.eval_func()
    if board.isGameOver():
        return stand_pat

    #stand_pat = board.eval_baier_func()
    if not whiteTurn:
        stand_pat = -stand_pat"""
    stand_pat = 0
    if whiteTurn:
        stand_pat = board.eval_baier_func()
    else:
        stand_pat = -board.eval_baier_func()

    if board.isGameOver():
        return stand_pat

    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.captureMoves(whiteTurn):
        new_board = LionBoard.LionBoard()
        new_board.setBoard(board)
        new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
        score = -quiescence_search(-beta, -alpha, new_board, not whiteTurn)
        if score > alpha:
            alpha = score
            bestmove = move
            if alpha >= beta:
                return beta
                #break
    return alpha

    """stand_pat = board.eval_baier_func()
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    if whiteTurn:
        maxEval = stand_pat
        list = board.captureMoves(whiteTurn)
        for move in list:
            new_board = LionBoard.LionBoard()
            new_board.setBoard(board)
            new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
            eval = quiescence_search(alpha, beta, new_board, not whiteTurn)
            if eval > maxEval:
                maxEval = eval
            alpha = max(alpha, eval)
            if beta <= alpha:
                return maxEval
        return alpha
    else:
        minEval = stand_pat
        list = board.captureMoves(whiteTurn)
        for move in list:
            new_board = LionBoard.LionBoard()
            new_board.setBoard(board)
            new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
            eval = quiescence_search(alpha, beta, new_board, not whiteTurn)
            if eval < minEval:
                minEval = eval
            beta = min(beta, eval)
            if beta <= alpha:
                return minEval
        return alpha
"""

    #GPT
    """eval = board.eval_func()

    if board.isGameOver():
        return eval

    stand_pat = eval
    if whiteTurn:
        for move in board.captureMoves(whiteTurn):
            new_board = LionBoard.LionBoard()
            new_board.setBoard(board)
            new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
            stand_pat = max(stand_pat, -quiescence_search(-beta, -alpha, new_board, not whiteTurn))
            alpha = max(alpha, stand_pat)
            if alpha >= beta:
                return alpha
    else:
        for move in board.captureMoves(whiteTurn):
            new_board = LionBoard.LionBoard()
            new_board.setBoard(board)
            new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
            stand_pat = min(stand_pat, -quiescence_search(-beta, -alpha, new_board, not whiteTurn))
            beta = min(beta, stand_pat)
            if alpha >= beta:
                return beta

    return stand_pat"""

def alpha_beta_quiescence(alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    """
    :param alpha: best of max player
    :param beta:  best of min player
    :param depth: depth left
    :param board: game state
    :param whiteTurn: white is max player, black min player
    :param moves: list of move that lead to this game state
    :return: eval, list of moves
    """
    evals = []
    #eval = board.eval_func()
    eval = board.eval_baier_func()

    if board.isGameOver():
        return eval, None, [eval]

    if depth == 0:
        if board.isQuiet():
            return eval, None, [eval]
        else:
            if whiteTurn:
                quiescence_eval = quiescence_search(alpha, beta, board, whiteTurn)
                # print("quiescence_eval:", quiescence_eval)
                # print("Eval:", eval)
                return quiescence_eval, None, [eval]
            else:
                quiescence_eval = - quiescence_search(alpha, beta, board, whiteTurn)
                # print("quiescence_eval:", quiescence_eval)
                # print("Eval:", eval)
                return quiescence_eval, None, [eval]
        """else:
            quiescence_eval = quiescence_search(alpha, beta, board, whiteTurn)
        #print("quiescence_eval:", quiescence_eval)
        #print("Eval:", eval)
        return quiescence_eval, None, [eval]"""


    if whiteTurn:
        maxEval = float('-inf')
        bestmove = Move.Move()
        #list = board.allpossibleMoves_Orderd(whiteTurn)
        #list = board.allpossibleMoves_baier_biglist(whiteTurn)
        #for move in list:
        list = board.allpossibleMoves_baier_capture(whiteTurn)
        for i in list:
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, Temp_Move, Temp = alpha_beta_quiescence(alpha, beta, depth - 1, new_board, new_white_turn)
                evals.append(eval)
                if eval > maxEval:
                    maxEval = eval
                    bestmove = move
                #elif eval == maxEval:
                #    rand = random.randint(0, 1)
                #    if rand == 1:
                #        bestmove = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    return maxEval, bestmove, evals
        return maxEval, bestmove, evals
    else:
        minEval = float('inf')
        bestmove = Move.Move()
        #list = board.allpossibleMoves_Orderd(whiteTurn)
        #list = board.allpossibleMoves_baier_biglist(whiteTurn)
        #for move in list:
        list = board.allpossibleMoves_baier_capture(whiteTurn)
        for i in list:
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, Temp_Move, Temp = alpha_beta_quiescence(alpha, beta, depth - 1, new_board, new_white_turn)
                evals.append(eval)
                if eval < minEval:
                    minEval = eval
                    bestmove = move
                #elif eval == minEval:
                #    rand = random.randint(0, 1)
                #    if rand == 1:
                #        bestmove = move
                beta = min(beta, eval)
                if beta <= alpha:
                    return minEval, bestmove, evals
        return minEval, bestmove, evals


def alpha_beta_quiescence_simple(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    eval, move, evals = alpha_beta_quiescence(float('-inf'), float('inf'), depth, board, whiteTurn)
    return eval, move, evals

def alpha_beta_quiescence_allMoves(alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool, moves: list):
    """
    :param alpha: best of max player
    :param beta:  best of min player
    :param depth: depth left
    :param board: game state
    :param whiteTurn: white is max player, black min player
    :param moves: list of move that lead to this game state
    :return: eval, list of moves
    """
    evals = []
    eval = board.eval_baier_func()

    if board.isGameOver():
        return eval, moves, [eval]

    if depth == 0:
        if board.isQuiet():
            return eval, moves, [eval]
        else:
            if whiteTurn:
                quiescence_eval = quiescence_search(alpha, beta, board, whiteTurn)
                # print("quiescence_eval:", quiescence_eval)
                # print("Eval:", eval)
                return quiescence_eval, moves, [eval]
            else:
                quiescence_eval = - quiescence_search(alpha, beta, board, whiteTurn)
                # print("quiescence_eval:", quiescence_eval)
                # print("Eval:", eval)
                return quiescence_eval, moves, [eval]

    best_moves = copy.deepcopy(moves)
    board_fen = board.getFen()

    if whiteTurn:
        maxEval = float('-inf')
        #list = board.allpossibleMoves(whiteTurn)
        list = board.allpossibleMoves_baier_capture(whiteTurn)
        for i in list:
            # print(len(i))
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_moves = copy.deepcopy(moves)
                new_moves.append(move)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, move_list, temp = alpha_beta_quiescence_allMoves(alpha, beta, depth - 1, new_board, new_white_turn, new_moves)
                evals.append(eval)
                if eval > maxEval:
                    maxEval = eval
                    best_moves = move_list
                alpha = max(alpha, eval)
                if beta <= alpha:
                    return maxEval, best_moves, evals
        return maxEval, best_moves, evals
    else:
        minEval = float('inf')
        #list = board.allpossibleMoves(whiteTurn)
        list = board.allpossibleMoves_baier_capture(whiteTurn)
        for i in list:
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_moves = copy.deepcopy(moves)
                new_moves.append(move)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, move_list, temp = alpha_beta_quiescence_allMoves(alpha, beta, depth - 1, new_board, new_white_turn, new_moves)
                evals.append(eval)
                if eval < minEval:
                    minEval = eval
                    best_moves = move_list
                beta = min(beta, eval)
                if beta <= alpha:
                    return minEval, best_moves, evals
        return minEval, best_moves, evals


def alpha_beta_quiescence_allMoves_simple(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    eval, moves, evals = alpha_beta_quiescence_allMoves(float('-inf'), float('inf'), depth, board, whiteTurn, [])
    return eval, moves, evals

def alpha_beta_win_loss(alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    """
    :param alpha: best of max player
    :param beta:  best of min player
    :param depth: depth left
    :param board: game state
    :param whiteTurn: white is max player, black min player
    :param moves: list of move that lead to this game state
    :return: eval, list of moves
    """
    eval = board.eval_win_loss()

    if depth == 0:
        return eval, None

    if board.isGameOver():
        return eval, None

    if whiteTurn:
        maxEval = float('-inf')
        bestmove = Move.Move()
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, Temp_Move = alpha_beta_win_loss(alpha, beta, depth - 1, new_board, new_white_turn)
                if eval > maxEval:
                    maxEval = eval
                    bestmove = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    return maxEval, bestmove
        return maxEval, bestmove
    else:
        minEval = float('inf')
        bestmove = Move.Move()
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_white_turn = not whiteTurn
                eval, Temp_Move = alpha_beta_win_loss(alpha, beta, depth - 1, new_board, new_white_turn)
                if eval < minEval:
                    minEval = eval
                    bestmove = move
                beta = min(beta, eval)
                if beta <= alpha:
                    return minEval, bestmove
        return minEval, bestmove


def alpha_beta_win_loss_simple(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    eval, move = alpha_beta_win_loss(float('-inf'), float('inf'), depth, board, whiteTurn)
    return eval, move

def NegaMax(alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    """if (game.isFinal()) {
    return player * game.score();
    for (int move: Game.moves) {
        game.doMove(move);
    int score = - scorePlayer(-player, -beta, -alpha); game.undoMove(move);
    if (score > alpha) {
    alpha = score;
    if (alpha >= beta)
    break;}
    }
    return alpha;}"""
    if whiteTurn:
        eval = board.eval_baier_func()
    else:
        eval = -board.eval_baier_func()

    if board.isGameOver():
        return eval, None

    if depth == 0:
        return eval, None

    bestmove = Move.Move()
    list = board.allpossibleMoves_baier_biglist(whiteTurn)
    for move in list:
        new_board = LionBoard.LionBoard()
        new_board.setBoard(board)
        new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
        eval, Temp_Move = NegaMax(-beta, -alpha, depth - 1, new_board, not whiteTurn)
        eval = -eval
        if eval > alpha:
            alpha = eval
            bestmove = move
            if alpha >= beta:
                break
    return alpha, bestmove


def MiniMax(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    if depth == 0:
        eval = board.eval_func()
        return eval, None

    if board.isGameOver():
        eval = board.eval_func()
        return eval, None

    if whiteTurn:
        maxEval = float('-inf')
        bestmove = Move.Move()
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                new_board = copy.deepcopy(board)
                #new_board = LionBoard.LionBoard()
                #new_board.setBoard(board)
                new_board.makeMove(True, move.getFrom(), move.getTo())
                #new_whiteTurn = not whiteTurn
                eval, temp_move = MiniMax(depth - 1, new_board, False)
                if eval > maxEval:
                    maxEval = eval
                    bestmove = move
        return maxEval, bestmove
    else:
        minEval = float('inf')
        bestmove = Move.Move()
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                new_board = copy.deepcopy(board)
                #new_board = LionBoard.LionBoard()
                #new_board.setBoard(board)
                new_board.makeMove(False, move.getFrom(), move.getTo())
                #new_whiteTurn = not whiteTurn
                eval, temp_move = MiniMax(depth - 1, new_board, True)
                if eval < minEval:
                    minEval = eval
                    bestmove = move
        return minEval, bestmove

def MiniMax_advanced(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    if depth == 0:
        eval = board.advanced_eval_func()
        return eval, None

    if board.isGameOver():
        eval = board.advanced_eval_func()
        return eval, None

    if whiteTurn:
        maxEval = float('-inf')
        bestmove = Move.Move()
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                # new_board = copy.deepcopy(board)
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_whiteTurn = not whiteTurn
                eval, temp_move = MiniMax_advanced(depth - 1, new_board, new_whiteTurn)
                if eval > maxEval:
                    maxEval = eval
                    bestmove = move
                elif eval == maxEval:
                    rand = random.randint(0, 1)
                    if rand == 1:
                        bestmove = move
        return maxEval, bestmove
    else:
        minEval = float('inf')
        bestmove = Move.Move()
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                # new_board = copy.deepcopy(board)
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_whiteTurn = not whiteTurn
                eval, temp_move = MiniMax_advanced(depth - 1, new_board, new_whiteTurn)
                if eval < minEval:
                    minEval = eval
                    bestmove = move
                elif eval == minEval:
                    rand = random.randint(0, 1)
                    if rand == 1:
                        bestmove = move
        return minEval, bestmove

"""def MiniMax(depth: int, board: LionBoard.LionBoard, whiteTurn: bool, moves: list):
    if depth == 0:
        eval = board.eval_func()
        return eval, moves

    if board.isGameOver():
        eval = board.eval_func()
        return eval, moves

    best_moves = copy.deepcopy(moves)

    if whiteTurn:
        maxEval = float('-inf')
        # bestmove = Move.Move()
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                # new_board = copy.deepcopy(board)
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_moves = copy.deepcopy(moves)
                new_moves.append(move)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_whiteTurn = not whiteTurn
                eval, move_list = MiniMax(depth - 1, new_board, new_whiteTurn, new_moves)
                if eval > maxEval:
                    maxEval = eval
                    best_moves = move_list
        return maxEval, best_moves
    else:
        minEval = float('inf')
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                # new_board = copy.deepcopy(board)
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_moves = copy.deepcopy(moves)
                new_moves.append(move)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                new_whiteTurn = not whiteTurn
                eval, move_list = MiniMax(depth - 1, new_board, new_whiteTurn, new_moves)
                if eval < minEval:
                    minEval = eval
                    best_moves = move_list
        return minEval, best_moves"""