import copy
import time
from Game import LionBoard, Zobrist
import random
from . import MTDfTranspositionsTable
from AlphaBeta import TranspostionTable, HashEntry

"""
Algorithm from https://askeplaat.wordpress.com/534-2/mtdf-algorithm/
"""

class MTDF:
    def __init__(self):
        self.zob = Zobrist.Zobrist()
        self.table = MTDfTranspositionsTable.TranspostionTable(25)
        self.count_transpo = 0
        self.count_MTDf_iter = 0
        self.TT = TranspostionTable.TranspostionTable(25)

    """function MTDF(root : node_type; f : integer; d: integer) : integer;

        g := f;
        upperbound := +INFINITY;
        lowerbound := -INFINITY;
        repeat
            if g == lowerbound then beta := g + 1 else beta := g;
            g := AlphaBetaWithMemory(root, beta – 1, beta, d);
            if g < beta then upperbound := g else lowerbound := g;
        until lowerbound >= upperbound;
        return g;"""

    def MTDF(self, f: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool, increment):
        #increment = 0.1
        g = f
        moves = []
        upperbound = float('inf')
        lowerbound = float('-inf')
        while not (lowerbound >= upperbound):
            self.count_MTDf_iter = self.count_MTDf_iter + 1
            beta = 0.0
            if g == lowerbound:
                beta = g + increment
            else:
                beta = g

            g, moves = self.alpha_beta_MTD(beta - increment, beta, depth, board, whiteTurn, [])

            if g < beta:
                upperbound = g
            else:
                lowerbound = g

        return g, moves

    def alpha_beta_MTD(self, alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool, moves: list):
        """
        :param alpha: best of max player
        :param beta:  best of min player
        :param depth: depth left
        :param board: game state
        :param whiteTurn: white is max player, black min player
        :param moves: list of move that lead to this game state
        :return: eval, list of moves
        """
        """boardhash = self.zob.generateHash(board, whiteTurn)
        entry = self.table.probeEntry(boardhash)
        if entry != None and len(moves) > 0:
            if entry.Depth >= depth:
                if entry.Lowerbound is not None:
                    if entry.Lowerbound >= beta:
                        self.count_transpo = self.count_transpo + 1
                        low = entry.Lowerbound
                        return low, moves
                    alpha = max(alpha, entry.Lowerbound)
                if entry.Upperbound is not None:
                    if entry.Upperbound >= alpha:
                        self.count_transpo = self.count_transpo + 1
                        up = entry.Upperbound
                        return up, moves
                    beta = min(beta, entry.Upperbound)"""

        # --------------------------------------------------
        """TT from AB"""
        boardhash = self.zob.generateHash(board, whiteTurn)
        boardFen = board.getFen()
        entry = self.TT.probeEntry(boardhash)
        # TT_Eval = 0
        # TT_used = False
        if entry != None and len(moves) > 0:
            if entry.whitetrun != whiteTurn:
                print("WhiteTurn miss match")
            if entry.Depth >= depth:
                self.count_transpo = self.count_transpo + 1
                TT_used = True
                TT_Eval = entry.Eval
                # print("TT used. Depth=", depth, " Entry Depth=", entry.Depth)
                return entry.Eval, moves
        # --------------------------------------------------

        g = 0.0
        best_moves = copy.deepcopy(moves)

        """if depth == 0:
        g = board.eval_func()"""

        """TT from AB"""
        if depth == 0:
            eval = board.eval_func()
            # if TT_used and TT_Eval != eval:
            #    print("Transpostion mismatch")
            newEntry = HashEntry.HashEntry(boardhash, depth, eval, boardFen, whiteTurn)
            self.table.storeEntry(newEntry)
            return eval, moves
        elif whiteTurn:
            g = float('-inf')
            a = alpha
            # bestmove = Move.Move()
            list = board.allpossibleMoves(whiteTurn)
            for i in list:
                # print(len(i))
                for move in i:
                    # new_board = copy.deepcopy(board)
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(move)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    eval, move_list = self.alpha_beta_MTD(a, beta, depth - 1, new_board, not whiteTurn, new_moves)
                    if eval > g:
                        g = eval
                        # bestmove = move
                        best_moves = move_list
                    elif eval == g:
                        # add a random element to selection of equal value
                        rand = random.randint(0, 1)
                        if rand == 1:
                            g = eval
                            # bestmove = move
                            best_moves = move_list
                    a = max(a, g)
                    if not(g < beta):
                        break
                else:
                    continue
                break
        else:
            g = float('inf')
            b = beta
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
                    eval, move_list = self.alpha_beta_MTD(alpha, b, depth - 1, new_board, not whiteTurn, new_moves)
                    if eval < g:
                        g = eval
                        # bestmove = move
                        best_moves = move_list
                    elif eval == g:
                        # add a random element to selection of equal value
                        rand = random.randint(0, 1)
                        if rand == 1:
                            g = eval
                            # bestmove = move
                            best_moves = move_list
                    b = min(beta, g)
                    if not(g > alpha):
                        break
                else:
                    continue
                break

        # --------------------------------------------------
        """TT from AB, store All"""
        newEntry = HashEntry.HashEntry(boardhash, depth, g, boardFen, whiteTurn)
        self.TT.storeEntry(newEntry)
        # --------------------------------------------------

        """if g <= alpha:
            self.table.storeUpperbound(boardhash, depth, g)
        if g > alpha and g < beta:
            self.table.storeLowerbound(boardhash, depth, g)
            self.table.storeUpperbound(boardhash, depth, g)
        if g >= beta:
            self.table.storeLowerbound(boardhash, depth, g)"""
        return g, best_moves

if __name__ == '__main__':
    board = LionBoard.LionBoard()
    board.setBoard_start()
    board.printBoard()
    mtd = MTDF()
    start = time.time()
    eval, moves = mtd.MTDF(0.0, 7, board, True)
    end = time.time()
    print(eval, " time:", (end - start))
    print("eval:", eval)
    print("transpos:", mtd.count_transpo)
    print("MTDf iter:", mtd.count_MTDf_iter)
    for i in moves:
        i.printMove()