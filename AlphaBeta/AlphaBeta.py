import copy
import time

from Game import LionBoard, Zobrist
import random
from . import TranspostionTable, HashEntry


class Alpha_Beta_TranspostionTable:
    def __init__(self):
        self.zob = Zobrist.Zobrist()
        self.table = TranspostionTable.TranspostionTable(25)
        self.count_transpo = 0

    def alpha_beta_TT(self, alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool,
                      moves: list, storeAll: bool):
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
        boardFen = board.getFen()
        entry = self.table.probeEntry(boardhash)
        # TT_Eval = 0
        # TT_used = False
        if entry != None and len(moves) > 0:
            if entry.Depth >= depth:
                self.count_transpo = self.count_transpo + 1
                TT_used = True
                TT_Eval = entry.Eval
                # print("TT used. Depth=", depth, " Entry Depth=", entry.Depth)
                return entry.Eval, moves

        if depth == 0:
            eval = board.eval_func()
            # if TT_used and TT_Eval != eval:
            #    print("Transpostion mismatch")
            newEntry = HashEntry.HashEntry(boardhash, depth, eval, boardFen)
            self.table.storeEntry(newEntry)
            return eval, moves

        best_moves = copy.deepcopy(moves)

        if whiteTurn:
            maxEval = float('-inf')
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
                    eval, move_list = self.alpha_beta_TT(alpha, beta, depth - 1, new_board, not whiteTurn, new_moves,
                                                         storeAll)
                    if eval > maxEval:
                        maxEval = eval
                        # bestmove = move
                        best_moves = move_list
                    elif eval == maxEval:
                        # add a random element to selection of equal value
                        rand = random.randint(0, 1)
                        if rand == 1:
                            maxEval = eval
                            # bestmove = move
                            best_moves = move_list
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                else:
                    continue
                break
            # moves.append(bestmove)

            if storeAll:
                newEntry = HashEntry.HashEntry(boardhash, depth, maxEval, boardFen)
                self.table.storeEntry(newEntry)

            """if TT_used and TT_Eval != maxEval:
                print("Transpostion mismatch")
            if TT_used:
                print("TT used")
                return TT_Eval, moves"""
            return maxEval, best_moves
        else:
            minEval = float('inf')
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
                    eval, move_list = self.alpha_beta_TT(alpha, beta, depth - 1, new_board, not whiteTurn, new_moves,
                                                         storeAll)
                    if eval < minEval:
                        minEval = eval
                        # bestmove = move
                        best_moves = move_list
                    elif eval == minEval:
                        # add a random element to selection of equal value
                        rand = random.randint(0, 1)
                        if rand == 1:
                            minEval = eval
                            # bestmove = move
                            best_moves = move_list
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                else:
                    continue
                break
            # moves.append(bestmove)

            if storeAll:
                newEntry = HashEntry.HashEntry(boardhash, depth, minEval, boardFen)
                self.table.storeEntry(newEntry)

            """if TT_used and TT_Eval != minEval:
                print("Transpostion mismatch")
            if TT_used:
                print("TT used")
                return TT_Eval, moves"""
            return minEval, best_moves

    def alpha_beta_TT_simple(self, depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
        eval, moves = self.alpha_beta_TT(float('-inf'), float('inf'), depth, board, whiteTurn, [], True)
        return eval, moves


def alpha_beta(alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool, moves: list):
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
        eval = board.eval_func()
        return eval, moves

    best_moves = copy.deepcopy(moves)

    if whiteTurn:
        maxEval = float('-inf')
        # bestmove = Move.Move()
        # best_moves = []
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
                eval, move_list = alpha_beta(alpha, beta, depth - 1, new_board, not whiteTurn, new_moves)
                if eval > maxEval:
                    maxEval = eval
                    # bestmove = move
                    best_moves = move_list
                elif eval == maxEval:
                    # add a random element to selection of equal value
                    rand = random.randint(0, 1)
                    if rand == 1:
                        maxEval = eval
                        # bestmove = move
                        best_moves = move_list
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            else:
                continue
            break
        # moves.append(bestmove)
        return maxEval, best_moves
    else:
        minEval = float('inf')
        # bestmove = Move.Move()
        # best_moves = []
        list = board.allpossibleMoves(whiteTurn)
        for i in list:
            for move in i:
                # new_board = copy.deepcopy(board)
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                new_moves = copy.deepcopy(moves)
                new_moves.append(move)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                eval, move_list = alpha_beta(alpha, beta, depth - 1, new_board, not whiteTurn, new_moves)
                if eval < minEval:
                    minEval = eval
                    # bestmove = move
                    best_moves = move_list
                elif eval == minEval:
                    # add a random element to selection of equal value
                    rand = random.randint(0, 1)
                    if rand == 1:
                        minEval = eval
                        # bestmove = move
                        best_moves = move_list
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            else:
                continue
            break
        # moves.append(bestmove)
        return minEval, best_moves


def alpha_beta_simple(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    eval, moves = alpha_beta(float('-inf'), float('inf'), depth, board, whiteTurn, [])
    return eval, moves


if __name__ == '__main__':
    board = LionBoard.LionBoard()
    board.setBoard_start()
    board.printBoard()
    ab = Alpha_Beta_TranspostionTable()

    print("First Board")
    start = time.time()
    eval, moves = alpha_beta_simple(7, board, True)
    end = time.time()
    print(eval, " time:", (end - start))

    start = time.time()
    eval, moves = ab.alpha_beta_TT_simple(7, board, True)
    end = time.time()
    print(eval, " time:", (end - start))
    print("transpos:", ab.count_transpo)

    """board.makeRandomMove(True)
    print("Next Board")

    start = time.time()
    eval, moves = alpha_beta_simple(7, board, False)
    end = time.time()
    print(eval, " time:", (end - start))

    start = time.time()
    eval, moves = ab.alpha_beta_TT_simple(7, board, False)
    end = time.time()
    print(eval, " time:", (end - start))
    print("transpos:", ab.count_transpo)

    board.makeRandomMove(False)
    print("Next Board")

    start = time.time()
    eval, moves = alpha_beta_simple(7, board, True)
    end = time.time()
    print(eval, " time:", (end - start))

    start = time.time()
    eval, moves = ab.alpha_beta_TT_simple(7, board, True)
    end = time.time()
    print(eval, " time:", (end - start))
    print("transpos:", ab.count_transpo)

    board.makeRandomMove(True)
    print("Next Board")

    start = time.time()
    eval, moves = alpha_beta_simple(7, board, False)
    end = time.time()
    print(eval, " time:", (end - start))

    start = time.time()
    eval, moves = ab.alpha_beta_TT_simple(7, board, False)
    end = time.time()
    print(eval, " time:", (end - start))
    print("transpos:", ab.count_transpo)

    board.makeRandomMove(False)
    print("Next Board")

    start = time.time()
    eval, moves = alpha_beta_simple(7, board, True)
    end = time.time()
    print(eval, " time:", (end - start))

    start = time.time()
    eval, moves = ab.alpha_beta_TT_simple(7, board, True)
    end = time.time()
    print(eval, " time:", (end - start))
    print("transpos:", ab.count_transpo)"""
