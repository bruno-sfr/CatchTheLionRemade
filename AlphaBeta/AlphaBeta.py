import copy
import time

from Game import LionBoard, Zobrist
import random
from . import TranspostionTable
from . import TranspostionTable_Flag
#import TranspostionTable
from . import HashEntry
from . import HashEntry_Flag
from . import AB_Flag
#import HashEntry


class Alpha_Beta_TranspostionTable:
    def __init__(self):
        self.zob = Zobrist.Zobrist()
        #self.table = TranspostionTable.TranspostionTable(20)
        self.table = TranspostionTable_Flag.TranspostionTable(20)
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
            # check if hash matches
            if entry.Hash == boardhash:
            #if entry.Fen == boardFen:
                if entry.Depth >= depth:
                #if entry.Depth == depth:
                    #eval , moves = alpha_beta(-100000, 1000000, depth, board, whiteTurn, [])
                    #if eval == entry.Eval:
                    #    self.count_transpo = self.count_transpo + 1
                    #    return entry.Eval, moves

                    self.count_transpo = self.count_transpo + 1
                    #TT_used = True
                    #TT_Eval = entry.Eval
                    # print("TT used. Depth=", depth, " Entry Depth=", entry.Depth)
                    return entry.Eval, moves
            else:
                #print("Hash dont match")
                pass

        #eval = board.eval_func()
        if depth == 0:
            eval = board.eval_func()
            # if TT_used and TT_Eval != eval:
            #    print("Transpostion mismatch")
            newEntry = HashEntry.HashEntry(boardhash, depth, eval, boardFen, whiteTurn)
            self.table.storeEntry(newEntry)
            return eval, moves

        #if eval > 900 or eval < -900:
        if board.isGameOver():
            eval = board.eval_func()
            return eval, moves

        best_moves = copy.deepcopy(moves)

        if whiteTurn:
            maxEval = float('-inf')
            # bestmove = Move.Move()
            list = board.allpossibleMoves(whiteTurn)
            for i in list:
                # print(len(i))
                for move in i:
                    #new_board = copy.deepcopy(board)
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(move)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    new_whiteTurn = not whiteTurn
                    eval, move_list = self.alpha_beta_TT(alpha, beta, depth - 1, new_board, new_whiteTurn, new_moves,
                                                         storeAll)
                    if eval > maxEval:
                        maxEval = eval
                        # bestmove = move
                        best_moves = move_list
                    #elif eval == maxEval:
                        # add a random element to selection of equal value
                    #    rand = random.randint(0, 1)
                    #    if rand == 1:
                    #        maxEval = eval
                            # bestmove = move
                    #        best_moves = move_list
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        return maxEval, best_moves
                        #break
                #else:
                #    continue
                #break
            # moves.append(bestmove)

            # chat gpt suggestion: alpha < maxEval < beta
            if storeAll and alpha < maxEval < beta:
                #eval, moves = alpha_beta(-100000, 1000000, depth, board, whiteTurn, [])
                #if eval != maxEval:
                #    pass
                """!!!!!!!!!!!!!!!!!!!!!!! not white turn seems very wrong"""
                newEntry = HashEntry.HashEntry(boardhash, depth, maxEval, boardFen, whiteTurn)
                #newEntry = HashEntry.HashEntry(boardhash, depth, maxEval, boardFen, not whiteTurn)
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
                    #new_board = copy.deepcopy(board)
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(move)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    new_whiteTurn = not whiteTurn
                    eval, move_list = self.alpha_beta_TT(alpha, beta, depth - 1, new_board, new_whiteTurn, new_moves,
                                                         storeAll)
                    if eval < minEval:
                        minEval = eval
                        # bestmove = move
                        best_moves = move_list
                    #elif eval == minEval:
                        # add a random element to selection of equal value
                    #    rand = random.randint(0, 1)
                    #    if rand == 1:
                    #        minEval = eval
                            # bestmove = move
                    #        best_moves = move_list
                    beta = min(beta, eval)
                    if beta <= alpha:
                        return minEval, best_moves
                        #break
                #else:
                #    continue
                #break
            # moves.append(bestmove)

            # chat gpt suggestion: alpha < maxEval < beta
            if storeAll and alpha < minEval < beta:
            #    eval, moves = alpha_beta(-100000, 1000000, depth, board, whiteTurn, [])
            #    if eval != minEval:
            #        pass
                """!!!!!!!!!!!!!!!!!!!!!!! not white turn seems very wrong"""
                newEntry = HashEntry.HashEntry(boardhash, depth, minEval, boardFen, whiteTurn)
                #newEntry = HashEntry.HashEntry(boardhash, depth, minEval, boardFen, not whiteTurn)
                self.table.storeEntry(newEntry)

            """if TT_used and TT_Eval != minEval:
                print("Transpostion mismatch")
            if TT_used:
                print("TT used")
                return TT_Eval, moves"""
            return minEval, best_moves

    def alpha_beta_TT_flag_gpt(self, alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool,
                        moves: list, storeAll: bool):
        boardhash = self.zob.generateHash(board, whiteTurn)
        boardFen = board.getFen()
        entry = self.table.probeEntry(boardhash)

        if entry is not None and len(moves) > 0:
            if entry.Hash == boardhash and entry.Depth >= depth:
                if entry.Flag == AB_Flag.Flag.EXACT:
                    return entry.Eval, moves
                elif entry.Flag == AB_Flag.Flag.LOWERBOUND:
                    alpha = max(alpha, entry.Eval)
                elif entry.Flag == AB_Flag.Flag.UPPERBOUND:
                    beta = min(beta, entry.Eval)

                if alpha >= beta:
                    return entry.Eval, moves

        if depth == 0 or board.isGameOver():
            eval = board.eval_func()
            flag = AB_Flag.Flag.EXACT
            if eval <= alpha:
                flag = AB_Flag.Flag.UPPERBOUND
            elif eval >= beta:
                flag = AB_Flag.Flag.LOWERBOUND
            newEntry = HashEntry_Flag.HashEntry(boardhash, depth, eval, boardFen, whiteTurn, flag)
            self.table.storeEntry(newEntry)
            return eval, moves

        best_moves = copy.deepcopy(moves)

        if whiteTurn:
            maxEval = float('-inf')
            list = board.allpossibleMoves(whiteTurn)
            for i in list:
                for move in i:
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(move)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    new_whiteTurn = not whiteTurn
                    eval, move_list = self.alpha_beta_TT_flag(alpha, beta, depth - 1, new_board, new_whiteTurn, new_moves,
                                                             storeAll)
                    if eval > maxEval:
                        maxEval = eval
                        best_moves = move_list
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        flag = AB_Flag.Flag.LOWERBOUND
                        if maxEval <= alpha:
                            flag = AB_Flag.Flag.UPPERBOUND
                        newEntry = HashEntry_Flag.HashEntry(boardhash, depth, maxEval, boardFen, whiteTurn, flag)
                        self.table.storeEntry(newEntry)
                        return maxEval, best_moves
            flag = AB_Flag.Flag.EXACT
            if maxEval <= alpha:
                flag = AB_Flag.Flag.UPPERBOUND
            elif maxEval >= beta:
                flag = AB_Flag.Flag.LOWERBOUND
            newEntry = HashEntry_Flag.HashEntry(boardhash, depth, maxEval, boardFen, whiteTurn, flag)
            self.table.storeEntry(newEntry)
            return maxEval, best_moves
        else:
            minEval = float('inf')
            list = board.allpossibleMoves(whiteTurn)
            for i in list:
                for move in i:
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(move)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    new_whiteTurn = not whiteTurn
                    eval, move_list = self.alpha_beta_TT_flag(alpha, beta, depth - 1, new_board, new_whiteTurn, new_moves,
                                                             storeAll)
                    if eval < minEval:
                        minEval = eval
                        best_moves = move_list
                    beta = min(beta, eval)
                    if beta <= alpha:
                        flag = AB_Flag.Flag.UPPERBOUND
                        if minEval >= beta:
                            flag = AB_Flag.Flag.LOWERBOUND
                        newEntry = HashEntry_Flag.HashEntry(boardhash, depth, minEval, boardFen, whiteTurn, flag)
                        self.table.storeEntry(newEntry)
                        return minEval, best_moves
            flag = AB_Flag.Flag.EXACT
            if minEval <= alpha:
                flag = AB_Flag.Flag.UPPERBOUND
            elif minEval >= beta:
                flag = AB_Flag.Flag.LOWERBOUND
            newEntry = HashEntry_Flag.HashEntry(boardhash, depth, minEval, boardFen, whiteTurn, flag)
            self.table.storeEntry(newEntry)
            return minEval, best_moves

    def alpha_beta_TT_flag(self, alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool,
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
            # check if hash matches
            if entry.Hash == boardhash:
            #if entry.Fen == boardFen:
                if entry.Depth == depth:
                    if entry.Flag == AB_Flag.Flag.EXACT:
                        return entry.Eval, moves
                        #if entry.Eval >= beta:
                        #    return entry.Eval, moves
                        #alpha = max(alpha, entry.Eval)
                        #if entry.Eval <= alpha:
                        #    return entry.Eval, moves
                        #beta = min(beta, entry.Eval)
                    elif entry.Flag == AB_Flag.Flag.LOWERBOUND:
                    #if entry.Flag == AB_Flag.Flag.LOWERBOUND:
                        # Update alpha with the lower bound
                        if entry.Eval >= beta:
                            return entry.Eval, moves
                        alpha = max(alpha, entry.Eval)
                    elif entry.Flag == AB_Flag.Flag.UPPERBOUND:
                        # Update beta with the upper bound
                        if entry.Eval <= alpha:
                            return entry.Eval, moves
                        beta = min(beta, entry.Eval)

        """if entry is not None and len(moves) > 0:
            if entry.Hash == boardhash and entry.Depth >= depth:
                if entry.Flag == AB_Flag.Flag.EXACT:
                    return entry.Eval, moves
                elif entry.Flag == AB_Flag.Flag.LOWERBOUND:
                    alpha = max(alpha, entry.Eval)
                elif entry.Flag == AB_Flag.Flag.UPPERBOUND:
                    beta = min(beta, entry.Eval)

                if alpha >= beta:
                    return entry.Eval, moves"""

        #eval = board.eval_func()
        if depth == 0:
            eval = board.eval_func()
            # if TT_used and TT_Eval != eval:
            #    print("Transpostion mismatch")
            newEntry = HashEntry_Flag.HashEntry(boardhash, depth, eval, boardFen, whiteTurn, AB_Flag.Flag.EXACT)
            self.table.storeEntry(newEntry)
            return eval, moves

        #if eval > 900 or eval < -900:
        if board.isGameOver():
            eval = board.eval_func()
            return eval, moves

        best_moves = copy.deepcopy(moves)

        if whiteTurn:
            maxEval = float('-inf')
            a = alpha
            # bestmove = Move.Move()
            list = board.allpossibleMoves(whiteTurn)
            for i in list:
                # print(len(i))
                for move in i:
                    #new_board = copy.deepcopy(board)
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(move)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    new_whiteTurn = not whiteTurn
                    eval, move_list = self.alpha_beta_TT_flag(a, beta, depth - 1, new_board, new_whiteTurn, new_moves, storeAll)
                    if eval > maxEval:
                        maxEval = eval
                        # bestmove = move
                        best_moves = move_list
                    #elif eval == maxEval:
                        # add a random element to selection of equal value
                    #    rand = random.randint(0, 1)
                    #    if rand == 1:
                    #        maxEval = eval
                            # bestmove = move
                    #        best_moves = move_list
                    a = max(a, eval)
                    #if beta <= alpha:
                    if not (maxEval < beta):
                        #newEntry = HashEntry_Flag.HashEntry(boardhash, depth, maxEval, boardFen, whiteTurn, AB_Flag.Flag.LOWERBOUND)
                        #self.table.storeEntry(newEntry)
                        #return maxEval, best_moves
                        break
                else:
                    continue
                break
            # moves.append(bestmove)
            if maxEval <= alpha:
                # Alpha Cutoff
                newEntry = HashEntry_Flag.HashEntry(boardhash, depth, maxEval, boardFen, whiteTurn, AB_Flag.Flag.UPPERBOUND)
                self.table.storeEntry(newEntry)
            elif alpha < maxEval < beta:
                newEntry = HashEntry_Flag.HashEntry(boardhash, depth, maxEval, boardFen, whiteTurn, AB_Flag.Flag.EXACT)
                self.table.storeEntry(newEntry)
            elif maxEval >= beta:
                # Beta Cutoff
                newEntry = HashEntry_Flag.HashEntry(boardhash, depth, maxEval, boardFen, whiteTurn, AB_Flag.Flag.LOWERBOUND)
                self.table.storeEntry(newEntry)
            #newEntry = HashEntry_Flag.HashEntry(boardhash, depth, maxEval, boardFen, whiteTurn, AB_Flag.Flag.EXACT)
            #self.table.storeEntry(newEntry)
            return maxEval, best_moves
        else:
            minEval = float('inf')
            b = beta
            # bestmove = Move.Move()
            list = board.allpossibleMoves(whiteTurn)
            for i in list:
                for move in i:
                    #new_board = copy.deepcopy(board)
                    new_board = LionBoard.LionBoard()
                    new_board.setBoard(board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(move)
                    new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    new_whiteTurn = not whiteTurn
                    eval, move_list = self.alpha_beta_TT_flag(alpha, b, depth - 1, new_board, new_whiteTurn, new_moves,
                                                         storeAll)
                    if eval < minEval:
                        minEval = eval
                        # bestmove = move
                        best_moves = move_list
                    #elif eval == minEval:
                        # add a random element to selection of equal value
                    #    rand = random.randint(0, 1)
                    #    if rand == 1:
                    #        minEval = eval
                            # bestmove = move
                    #        best_moves = move_list
                    b = min(b, eval)
                    #if beta <= alpha:
                    if not(minEval > alpha):
                        #newEntry = HashEntry_Flag.HashEntry(boardhash, depth, minEval, boardFen, whiteTurn,AB_Flag.Flag.UPPERBOUND)
                        #self.table.storeEntry(newEntry)
                        #return minEval, best_moves
                        break
                else:
                    continue
                break
            # moves.append(bestmove)

            if minEval <= alpha:
                # Alpha Cutoff
                newEntry = HashEntry_Flag.HashEntry(boardhash, depth, minEval, boardFen, whiteTurn, AB_Flag.Flag.UPPERBOUND)
                self.table.storeEntry(newEntry)
            elif alpha < minEval < beta:
                newEntry = HashEntry_Flag.HashEntry(boardhash, depth, minEval, boardFen, whiteTurn, AB_Flag.Flag.EXACT)
                self.table.storeEntry(newEntry)
            elif minEval >= beta:
                # Beta Cutoff
                newEntry = HashEntry_Flag.HashEntry(boardhash, depth, minEval, boardFen, whiteTurn, AB_Flag.Flag.LOWERBOUND)
                self.table.storeEntry(newEntry)
            #newEntry = HashEntry_Flag.HashEntry(boardhash, depth, minEval, boardFen, whiteTurn, AB_Flag.Flag.EXACT)
            #self.table.storeEntry(newEntry)
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
    eval = board.eval_func()

    if depth == 0:
        #eval = board.eval_func()
        return eval, moves

    #if eval > 900 or eval < -900:
    if board.isGameOver():
        return eval, moves

    best_moves = copy.deepcopy(moves)
    board_fen = board.getFen()

    if whiteTurn:
        maxEval = float('-inf')
        # bestmove = Move.Move()
        # best_moves = []
        list = board.allpossibleMoves(whiteTurn)
        #list = reversed(list)
        for i in list:
            # print(len(i))
            for move in i:
                #new_board = copy.deepcopy(board)
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                #new_board.setBoard_Fen(board.getFen())
                new_moves = copy.deepcopy(moves)
                new_moves.append(move)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                #if new_board.makeMove(whiteTurn, move.getFrom(), move.getTo()):
                #    pass
                #else:
                #   pass
                #history_1 = len(board.Move_History)
                #board_fen = board.getFen()
                #board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                #if board.makeMove(whiteTurn, move.getFrom(), move.getTo()):
                #    pass
                #else:
                #    pass
                #history_2 = len(board.Move_History)
                #if history_1 == history_2:
                #    pass
                new_white_turn = not whiteTurn
                eval, move_list = alpha_beta(alpha, beta, depth - 1, new_board, new_white_turn, new_moves)
                #eval, move_list = alpha_beta(alpha, beta, depth - 1, board, new_white_turn, new_moves)
                #if depth == 6:
                #    pass
                #try:
                #    board.reverse_last_move()
                #except Exception as e:
                #    print(e)
                #fen_after_reversed = board.getFen()
                #if board_fen != fen_after_reversed:
                #    pass
                if eval > maxEval:
                    maxEval = eval
                    # bestmove = move
                    best_moves = move_list
                #elif eval == maxEval:
                    # add a random element to selection of equal value
                #    rand = random.randint(0, 1)
                #    if rand == 1:
                #        maxEval = eval
                        # bestmove = move
               #         best_moves = move_list
                alpha = max(alpha, eval)
                if beta <= alpha:
                    return maxEval, best_moves
                    #break
            #else:
            #    continue
            #break
        # moves.append(bestmove)
        return maxEval, best_moves
    else:
        minEval = float('inf')
        # bestmove = Move.Move()
        # best_moves = []
        list = board.allpossibleMoves(whiteTurn)
        #list = reversed(list)
        for i in list:
            for move in i:
                #new_board = copy.deepcopy(board)
                new_board = LionBoard.LionBoard()
                new_board.setBoard(board)
                #new_board.setBoard_Fen(board.getFen())
                new_moves = copy.deepcopy(moves)
                new_moves.append(move)
                new_board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                #if new_board.makeMove(whiteTurn, move.getFrom(), move.getTo()):
                #    pass
                #else:
                #    pass
                #history_1 = len(board.Move_History)
                #board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                #history_2 = len(board.Move_History)
                #if history_1 == history_2:
                #    pass
                new_white_turn = not whiteTurn
                eval, move_list = alpha_beta(alpha, beta, depth - 1, new_board, new_white_turn, new_moves)
                #eval, move_list = alpha_beta(alpha, beta, depth - 1, board, new_white_turn, new_moves)
                #try:
                #    board.reverse_last_move()
                #except Exception as e:
                #    print(e)
                #fen_after_reversed = board.getFen()
                #if board_fen != fen_after_reversed:
                #    pass
                #if depth == 7:
                #    pass
                if eval < minEval:
                    minEval = eval
                    # bestmove = move
                    best_moves = move_list
                #elif eval == minEval:
                    # add a random element to selection of equal value
                #    rand = random.randint(0, 1)
                #    if rand == 1:
                #        minEval = eval
                        # bestmove = move
                #        best_moves = move_list
                beta = min(beta, eval)
                if beta <= alpha:
                    return minEval, best_moves
                    #break
            #else:
            #    continue
            #break
        # moves.append(bestmove)
        return minEval, best_moves


def alpha_beta_simple(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    eval, moves = alpha_beta(float('-inf'), float('inf'), depth, board, whiteTurn, [])
    return eval, moves


def alpha_beta_win_loss(alpha: float, beta: float, depth: int, board: LionBoard.LionBoard, whiteTurn: bool,
                        moves: list):
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
        return eval, moves

    if board.isGameOver():
        return eval, moves

    best_moves = copy.deepcopy(moves)

    if whiteTurn:
        #maxEval = float('-inf')
        maxEval = -1
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
                eval, move_list = alpha_beta_win_loss(alpha, beta, depth - 1, new_board, not whiteTurn, new_moves)
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
        #minEval = float('inf')
        minEval = 1
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
                eval, move_list = alpha_beta_win_loss(alpha, beta, depth - 1, new_board, not whiteTurn, new_moves)
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


def alpha_beta_win_loss_simple(depth: int, board: LionBoard.LionBoard, whiteTurn: bool):
    eval, moves = alpha_beta_win_loss(float('-inf'), float('inf'), depth, board, whiteTurn, [])
    return eval, moves


if __name__ == '__main__':
    board = LionBoard.LionBoard()

    board.setBoard_start()
    #board.setBoard_Fen("elc/1C1/G1E/1L1/g")

    #board.setBoard_Fen("gl1/1Cg/L2/2E/cE")
    board.setBoard_Fen("el1/1Cg/L2/2E/cE")
    #board.setBoard_Fen("g11/1lg/111/L1h/ceE")

    #board.makeMove(False, 6, 9)
    #board.makeMove(False, 'c', 9)
    #board.makeMove(False,'c',8)
    #board.makeMove(False, 'c', 3)
    #board.makeMove(True,7,10)
    #board.setBoard_Fen("glc/1CG/L2/2E/E")
    board.printBoard()

    start = time.time()
    eval, moves = alpha_beta_simple(7, board, False)
    #eval, moves = alpha_beta_simple(6, board, True)
    #eval, moves = alpha_beta(float('-inf'), -8.25, 6, board, True, [])
    end = time.time()
    print("time:", (end - start))
    #eval, moves = alpha_beta(-100000, -8.5, 6, board, True, [])
    #eval, moves = alpha_beta_simple(6, board, True)

    print("eval:", eval)
    for i in moves:
        i.printMove()

    """board.setBoard_Fen("g11/1lg/111/L1h/ceE")
    board.printBoard()
    board.makeMove(True, 2, 1)
    eval, moves = alpha_beta_simple(1, board, False)
    board.printBoard()
    board.reverse_last_move()
    board.printBoard()"""

    """board = LionBoard.LionBoard()
    #board.setBoard_start()
    board.setBoard_Fen("elc/1C1/G11/1LE/G")
    board.printBoard()
    ab = Alpha_Beta_TranspostionTable()

    list = board.allpossibleMoves_BigList(True)

    board.makeMove(True,7,10)

    print(board.eval_func())

    #start = time.time()
    eval, moves = ab.alpha_beta_TT_simple(7, board, False)
    moves[0].printMove()
    print("Eval:", eval)

    eval, moves = alpha_beta_simple(7, board, False)
    #end = time.time()
    moves[0].printMove()
    print("Eval:", eval)
    #print(eval, " time:", (end - start))"""

    """print("First Board")
    start = time.time()
    eval, moves = alpha_beta_simple(7, board, True)
    end = time.time()
    print(eval, " time:", (end - start))"""

    """start = time.time()
    eval, moves = ab.alpha_beta_TT_simple(10, board, True)
    end = time.time()
    print(eval, " time:", (end - start))
    print("transpos:", ab.count_transpo)"""

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
