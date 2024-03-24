import datetime
import math
import random
import time

import matplotlib.pyplot as plt

from AlphaBeta import AlphaBeta
from Game import LionBoard
from MonteCarlo import MCTS_Solvers


def AB_VS_AB():
    board = LionBoard.LionBoard()
    board.setBoard_start()
    #board.setBoard_Fen("11l/1ce/11L/1C1/EGG")
    #board.setBoard_Fen("11l/1L1/3/3/")
    board.setBoard_Fen("3/11l/1L1/3/")
    #board.setBoard_Fen("1l1/Gg1/1Ee/2L/cC")
    board.printBoard()
    """whiteTurn = True
    board.makeMove(True, 'g', 11)
    board.makeMove(False, 6, 10)
    board.makeMove(True, 'g', 0)
    board.makeMove(False, 10, 6)
    board.makeMove(True, 'e', 2)
    evalAB, moves, evals = AlphaBeta.alpha_beta_quiescence_simple(1, board, False)
    print("White Player Eval:", evalAB)
    for eval in evals:
        print("possible Eval:", eval)
    #for move in moves:
    #    move.printMove()"""
    """for i in range(10):
        print("-----------------------------------  Depth ",i)
        evalAB, moves, evals = AlphaBeta.alpha_beta_allMoves_simple(i, board, whiteTurn)
        print("White Player Eval:", evalAB)
        for eval in evals:
            print("possible Eval:", eval)
        for move in moves:
            move.printMove()"""

    #print(board.hasCaptures(True))
    #print(board.isCheck())

    count = 1
    list = board.allpossibleMoves_baier_capture(True)
    for ilist in list:
        print("List ",count)
        count = count + 1
        for i in ilist:
            i.printMove()

    """eval, move = AlphaBeta.alpha_beta_quiescence_simple(6, board, True)
    print("Eval", eval)
    move.printMove()"""

    """evalAB, moves, evals = AlphaBeta.alpha_beta_allMoves_simple(7, board, whiteTurn)
    print("White Player Eval:", evalAB)
    for eval in evals:
        print("possible Eval:", eval)
    for move in moves:
        move.printMove()"""

    """whiteTurn = True

    while not board.isGameOver():
        if whiteTurn:
            evalAB, moves, evals = AlphaBeta.alpha_beta_allMoves_simple(6, board, whiteTurn)
            print("White Player Eval:", evalAB)
            for eval in evals:
                print("possible Eval:",eval)
            for move in moves:
                move.printMove()
            print("----Making-Move----")
            board.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo())
            print("New FEN:",board.getFen())
        else:
            evalAB, moves, evals = AlphaBeta.alpha_beta_allMoves_simple(7, board, whiteTurn)
            print("Black Player Eval:", evalAB)
            for eval in evals:
                print("possible Eval:",eval)
            for move in moves:
                move.printMove()
            print("----Making-Move----")
            board.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo())
            print("New FEN:", board.getFen())
        whiteTurn = not whiteTurn
    board.printBoard()"""

    """while not board.isGameOver():
        if whiteTurn:
            evalAB, move, evals = AlphaBeta.alpha_beta_quiescence_simple(6, board, whiteTurn)
            print("White Player Eval:", evalAB)
            for eval in evals:
                print("possible Eval:", eval)
            move.printMove()
            print("----Making-Move----")
            print("")
            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
            print("New FEN:", board.getFen())
        else:
            evalAB, move, evals = AlphaBeta.alpha_beta_quiescence_simple(7, board, whiteTurn)
            print("Black Player Eval:", evalAB)
            for eval in evals:
                print("possible Eval:", eval)
            move.printMove()
            print("----Making-Move----")
            print("")
            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
            print("New FEN:", board.getFen())
        whiteTurn = not whiteTurn
    board.printBoard()"""

def TestPostion():
    board = LionBoard.LionBoard()
    board.setBoard_start()
    whiteTurn = True
    evalMTD_even = 0.0
    evalMTD_uneven = 0.0

    AB_List = []
    MM_List = []
    AB_TT_store_List = []
    MTD_second_guess_List = []

    AB_Eval_List = []
    MM_Eval_List = []
    AB_TT_store_Eval_List = []
    MTD_second_guess_Eval_List = []

    #AB= AlphaBeta.Alpha_Beta_TT()
    MTD_second_guess = AlphaBeta.MTDF()

    Depth = 6
    iterations = 1
    x = range(1, Depth + 1)

    for i in range(1, Depth + 1):
        print("Depth:", i)
        print("Alpha-Beta")
        avg_timetaken = 0
        for i2 in range(iterations):
            start = time.time()
            evalAB, moves = AlphaBeta.alpha_beta_simple(i, board, whiteTurn)
            end = time.time()
            print("eval:", evalAB)
            timetaken = (end - start)
            moves.printMove()
            #print("timetaken", timetaken)
            avg_timetaken = avg_timetaken + timetaken
        avg_timetaken = avg_timetaken/iterations
        #print("avg time:", avg_timetaken)
        AB_List.append(avg_timetaken)
        #AB_Eval_List.append(evalAB)

        print("")
        print("MiniMax")
        avg_timetaken = 0
        for i2 in range(iterations):
            start = time.time()
            evalMM, moves = AlphaBeta.MiniMax(i, board, whiteTurn)
            print("eval:", evalMM)
            moves.printMove()
            end = time.time()
            timetaken = (end - start)
            #print("timetaken", timetaken)
            avg_timetaken = avg_timetaken + timetaken
        avg_timetaken = avg_timetaken / iterations
        #print("avg time:", avg_timetaken)
        MM_List.append(avg_timetaken)
        #MM_Eval_List.append(evalMM)

        """print("")
        print("Alpha-Beta_TT")
        avg_timetaken = 0
        for i2 in range(iterations):
            AB = AlphaBeta.Alpha_Beta_TT()
            start = time.time()
            eval, move = AB.alpha_beta_TT_simple(i, board, whiteTurn)
            #print("eval:", eval)
            end = time.time()
            timetaken = (end - start)
            print("timetaken:", timetaken)
            avg_timetaken = avg_timetaken + timetaken
        avg_timetaken = avg_timetaken / iterations
        print("avg time:", avg_timetaken)
        AB_TT_store_List.append(avg_timetaken)"""
        #AB_TT_store_Eval_List.append(eval)

        """print("")
        print("MTD(f) with f=bestSecondGuess")
        avg_timetaken = 0
        for i2 in range(iterations):
            MTD_second_guess = AlphaBeta.MTDF()
            start = time.time()
            if i % 2 == 0:
                evalMTD_even, movesMTD = MTD_second_guess.MTDF(evalMTD_even, i, board, whiteTurn, 0.1)
                #print("eval:", evalMTD_even)
            else:
                evalMTD_uneven, movesMTD = MTD_second_guess.MTDF(evalMTD_uneven, i, board, whiteTurn, 0.1)
                #print("eval:", evalMTD_uneven)
            end = time.time()
            timetaken = (end - start)
            print("timetaken:",timetaken)
            avg_timetaken = avg_timetaken + timetaken
        avg_timetaken = avg_timetaken / iterations
        print("avg time:", avg_timetaken)
        MTD_second_guess_List.append(avg_timetaken)"""
        print("----------------------------------")
    print("Benchmark complete")

    """x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    plt.plot(x, MM_List, label='MiniMax', color='magenta')
    plt.plot(x, AB_List, label='Alpha-Beta', color='red')
    plt.plot(x, AB_TT_store_List, label='Alpha-Beta TT', color='blue')
    plt.plot(x, MTD_second_guess_List, label='MTD(f)', color='green')
    plt.legend(loc='upper left')"""

    """fig, axs = plt.subplots(2, sharex=True)
    fig.suptitle("Comparison")

    #axs[0].plot(x, MM_List, label='MiniMax')
    axs[0].plot(x, AB_List, label='Alpha-Beta')
    #axs[0].plot(x, AB_TT_List, label='Alpha-Beta TT', linestyle='dotted')
    axs[0].plot(x, AB_TT_store_List, label='Alpha-Beta TT Store All', linestyle='dashed')
    #axs[0].plot(x, MTD_List, label='MTD(f) with f = best guess', linestyle='dashed')
    axs[0].plot(x, MTD_second_guess_List, label='MTD(f) with f = best second guess', linestyle='dashed')
    #axs[0].plot(x, MTD_MiniMax_List, label='MTD(f) with f = BestMiniMax', linestyle='dashdot')
    #axs[0].plot(x, MTD_0_List, label='MTD(f) with f = 0', linestyle='dashed')
    #axs[0].plot(x, MTD_no_TT_List, label='MTD(f) with no TT', linestyle='dashdot')
    #axs[0].plot(x, MTD_2_TT_List, label='MTD(f) with 2 TT', linestyle='dashdot')
    axs[0].set(ylabel='Time taken')

    axs[0].legend(loc='upper left')

    #axs[1].plot(x, MM_Eval_List, label='MiniMax')
    axs[1].plot(x, AB_Eval_List, label='Alpha-Beta')
    #axs[1].plot(x, AB_TT_Eval_List, label='Alpha-Beta TT', linestyle='dotted')
    axs[1].plot(x, AB_TT_store_Eval_List, label='Alpha-Beta TT Store All', linestyle='dashed')
    #axs[1].plot(x, MTD_Eval_List, label='MTD(f) with f = best guess', linestyle='dashed')
    axs[1].plot(x, MTD_second_guess_Eval_List, label='MTD(f) with f = second best guess', linestyle='dashed')
    #axs[1].plot(x, MTD_MiniMax_Eval_List, label='MTD(f) with f = BestMiniMax', linestyle='dashdot')
    #axs[1].plot(x, MTD_0_Eval_List, label='MTD(f) with f = 0', linestyle='dashed')
    #axs[1].plot(x, MTD_no_TT_Eval_List, label='MTD(f) with no TT', linestyle='dashdot')
    #axs[1].plot(x, MTD_2_TT_Eval_List, label='MTD(f) with 2 TT', linestyle='dashdot')
    axs[1].set(ylabel='Eval')"""

    """plt.xlabel("Depth")
    plt.ylabel("Time taken in s")
    plt.title("Comparison of MiniMax-Algorithms on Start Position")
    plt.savefig(f"../Resources/Benchmark_Start_Pos_Depth_{Depth}_{iterations}.png")
    plt.show()"""

def Mate_in_Benchmark():
    board = LionBoard.LionBoard()
    Depth = 5
    MM_List = [0] * (Depth)
    AB_List = [0] * (Depth)
    MTD_List = [0] * (Depth)
    AB_TT_store_List = [0] * (Depth)
    x = range(1, Depth + 1)
    iterations = 1
    boards = ["eg1/lc1/1CL/G1E/", "eg1/1l1/GE1/1L1/cC", "1l1/G2/L1g/2E/cCE", "eg1/lc1/1CL/G1E/", "1g1/G1l/3/1LE/cC"]

    for fen in boards:
        board.setBoard_Fen(fen)
        MTD = AlphaBeta.MTDF()
        AB = AlphaBeta.Alpha_Beta_TT()

        evalMTD_even = 0.0
        evalMTD_uneven = 0.0
        for i in range(1, Depth+1):
            print("Depth:", i)
            print("MiniMax")
            avg_timetaken = 0
            for i2 in range(iterations):
                start = time.time()
                evalMM, moves = AlphaBeta.MiniMax(i, board, True)
                #evalMM, moves = AlphaBeta.MiniMax_advanced(i, board, True)
                print("eval:", evalMM)
                moves.printMove()
                end = time.time()
                timetaken = (end - start)
                print("timetaken", timetaken)
                avg_timetaken = avg_timetaken + timetaken
            avg_timetaken = avg_timetaken / iterations
            print("avg time:", avg_timetaken)
            # moves.printMove()
            MM_List[i - 1] = MM_List[i - 1] + avg_timetaken

            print("")
            print("Alpha-Beta")
            avg_timetaken = 0
            for i2 in range(iterations):
                start = time.time()
                evalAB, moves = AlphaBeta.alpha_beta_simple(i, board, True)
                #evalAB, moves = AlphaBeta.alpha_beta_advanced_simple(i, board, True)
                end = time.time()
                moves.printMove()
                print("eval:", evalAB)
                timetaken = (end - start)
                print("timetaken", timetaken)
                avg_timetaken = avg_timetaken + timetaken
            avg_timetaken = avg_timetaken / iterations
            print("avg time:", avg_timetaken)
            AB_List[i-1] = AB_List[i-1] + avg_timetaken

            print("")
            print("Alpha-Beta_TT")
            avg_timetaken = 0
            for i2 in range(iterations):
                AB = AlphaBeta.Alpha_Beta_TT()
                start = time.time()
                eval, move = AB.alpha_beta_TT_simple(i, board, True)
                #eval, move = AB.alpha_beta_advanced_TT_simple(i, board, True)
                print("eval:", eval)
                move.printMove()
                end = time.time()
                timetaken = (end - start)
                print("timetaken:", timetaken)
                avg_timetaken = avg_timetaken + timetaken
            avg_timetaken = avg_timetaken / iterations
            print("avg time:", avg_timetaken)
            AB_TT_store_List[i - 1] = AB_TT_store_List[i - 1] + avg_timetaken

            print("")
            print("MTD(f) with f=bestGuess")
            avg_timetaken = 0
            for i2 in range(iterations):
                MTD_second_guess = AlphaBeta.MTDF()
                start = time.time()
                if i % 2 == 0:
                    evalMTD_even, movesMTD = MTD_second_guess.MTDF(evalMTD_even, i, board, True, 0.1)
                    #evalMTD_even, movesMTD = MTD_second_guess.MTDF_advanced(evalMTD_even, i, board, True, 0.1)
                    print("eval:", evalMTD_even)
                    movesMTD.printMove()
                else:
                    evalMTD_uneven, movesMTD = MTD_second_guess.MTDF(evalMTD_uneven, i, board, True, 0.1)
                    #evalMTD_uneven, movesMTD = MTD_second_guess.MTDF_advanced(evalMTD_uneven, i, board, True, 0.1)
                    print("eval:", evalMTD_uneven)
                    movesMTD.printMove()
                end = time.time()
                timetaken = (end - start)
                print("timetaken:", timetaken)
                avg_timetaken = avg_timetaken + timetaken
            avg_timetaken = avg_timetaken / iterations
            print("avg time:", avg_timetaken)
            MTD_List[i - 1] = MTD_List[i - 1] + avg_timetaken
            print("----------------------------------")
        print("Board done!")
        print("----------------------------------")
    print("Benchmark complete")

    for i in range(0, Depth-1):
        #MM_List[i] = MM_List[i] / len(boards)
        AB_List[i] = AB_List[i] / len(boards)
        AB_TT_store_List[i] = AB_TT_store_List[i] / len(boards)
        MTD_List[i] = MTD_List[i] / len(boards)

    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    #plt.plot(x, MM_List, label='MiniMax')
    plt.plot(x, AB_List, label='Alpha-Beta')
    plt.plot(x, AB_TT_store_List, label='Alpha-Beta TT')
    plt.plot(x, MTD_List, label='MTD')
    plt.xlabel("Depth")
    plt.ylabel("Time taken in s")
    plt.title("Benchmark Mate in 3")
    plt.legend()
    plt.savefig(f"../Resources/Benchmark_Mate_in_3.png")
    plt.show()

def Testing_PV():
    board = LionBoard.LionBoard()
    """board.setBoard_start()
    print("start_eval", board.eval_func())
    board.makeMove(False,7,4)
    print("next_eval", board.eval_func())"""
    #board.randomBoard()

    board.setBoard_start()

    #Mate in Puzzle
    #board.setBoard_Fen("eg1/lc1/1CL/G1E/")
    #board.setBoard_Fen("eg1/1l1/GE1/1L1/cC")
    #board.setBoard_Fen("1l1/G2/L1g/2E/cCE")
    #board.setBoard_Fen("eg1/lc1/1CL/G1E/")
    #board.setBoard_Fen("1g1/G1l/3/1LE/cC")
    #board.setBoard_Fen("1l1/Ge1/L1g/2E/cC")

    whiteTurn = True

    #Generell
    #board.setBoard_Fen("1l1/Gg1/1Ee/2L/cC")
    #board.setBoard_Fen("el1/1c1/GCg/1LE/")
    "best move 1 to 3"
    #board.setBoard_Fen("1l1/1e1/1Gg/1LE/Cc")
    "best move 3 to 4"
    board.printBoard()
    print("WhiteTurn =", whiteTurn)
    print("")

    Depth = 6

    for i in reversed(range(Depth + 1)):
        if i == 0:
            return
        print("Depth ",i)
        evalAB, moves, evals = AlphaBeta.alpha_beta_allMoves_simple(i, board, whiteTurn)
        print("Eval:", evalAB)
        for move in moves:
            move.printMove()
        print("----Making-Move----")
        board.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo())
        if (board.isGameOver()):
            board.printBoard()
            return
        whiteTurn = not whiteTurn

    """print("Depth 6")
    evalAB, moves = AlphaBeta.alpha_beta_allMoves_simple(6, board, False)
    print("Eval:", evalAB)
    for move in moves:
        move.printMove()
    print("----Making-Move----")
    board.makeMove(False, moves[0].getFrom(), moves[0].getTo())
    if (board.isGameOver()):
        board.printBoard()
        return

    print("Depth 5")
    evalAB, moves = AlphaBeta.alpha_beta_allMoves_simple(5, board, True)
    print("Eval:", evalAB)
    for move in moves:
        move.printMove()
    print("----Making-Move----")
    board.makeMove(True, moves[0].getFrom(), moves[0].getTo())
    if (board.isGameOver()):
        board.printBoard()
        return

    print("Depth 4")
    evalAB, moves = AlphaBeta.alpha_beta_allMoves_simple(6, board, False)
    print("Eval:", evalAB)
    for move in moves:
        move.printMove()
    print("----Making-Move----")
    board.makeMove(False, moves[0].getFrom(), moves[0].getTo())
    if (board.isGameOver()):
        board.printBoard()
        return"""

    """print("-----------------------------------")

    print("Depth 7")
    evalAB, moves = AlphaBeta.alpha_beta_allMoves_simple(7, board, True)
    print("Eval:", evalAB)
    for move in moves:
        move.printMove()
    print("----Making-Move----")
    board.makeMove(True, moves[0].getFrom(), moves[0].getTo())
    if (board.isGameOver()):
        board.printBoard()
        return

    print("Depth 6")
    evalAB, moves = AlphaBeta.alpha_beta_allMoves_simple(6, board, False)
    print("Eval:", evalAB)
    for move in moves:
        move.printMove()
    print("----Making-Move----")
    board.makeMove(False, moves[0].getFrom(), moves[0].getTo())
    if (board.isGameOver()):
        board.printBoard()
        return

    print("Depth 5")
    evalAB, moves = AlphaBeta.alpha_beta_allMoves_simple(5, board, True)
    print("Eval:",evalAB)
    for move in moves:
        move.printMove()
    print("----Making-Move----")
    board.makeMove(True, moves[0].getFrom(), moves[0].getTo())
    if(board.isGameOver()):
        board.printBoard()
        return

    print("Depth 4")
    evalAB, moves = AlphaBeta.alpha_beta_allMoves_simple(4, board, False)
    print("Eval:", evalAB)
    for move in moves:
        move.printMove()
    print("----Making-Move----")
    board.makeMove(False, moves[0].getFrom(), moves[0].getTo())
    if (board.isGameOver()):
        board.printBoard()
        return

    print("Depth 3")
    evalAB, moves = AlphaBeta.alpha_beta_allMoves_simple(3, board, True)
    print("Eval:", evalAB)
    for move in moves:
        move.printMove()
    print("----Making-Move----")
    board.makeMove(True, moves[0].getFrom(), moves[0].getTo())
    if (board.isGameOver()):
        board.printBoard()
        return

    print("Depth 2")
    evalAB, moves = AlphaBeta.alpha_beta_allMoves_simple(2, board, False)
    print("Eval:", evalAB)
    for move in moves:
        move.printMove()
    print("----Making-Move----")
    board.makeMove(False, moves[0].getFrom(), moves[0].getTo())
    if (board.isGameOver()):
        board.printBoard()
        return

    print("Depth 1")
    evalAB, moves = AlphaBeta.alpha_beta_allMoves_simple(1, board, True)
    print("Eval:", evalAB)
    for move in moves:
        move.printMove()
    print("----Making-Move----")
    board.makeMove(True, moves[0].getFrom(), moves[0].getTo())

    if (board.isGameOver()):
        board.printBoard()
        return"""

def Random_Benchmark():
    board = LionBoard.LionBoard()

    Depth = 8
    Iterations = 5

    AB_List = [0] * (Depth)
    MTD_List = [0] * (Depth )
    AB_TT_store_List = [0] * (Depth)
    x = range(1, Depth + 1)

    for i2 in range(0, Iterations):
        board.randomBoard()
        MTD = AlphaBeta.MTDF()
        AB = AlphaBeta.Alpha_Beta_TT()

        evalMTD = 0.0
        evalMTD_no_tt = 0.0
        for i in range(1, Depth+1):
            print("Depth:", i)
            print("Alpha-Beta")
            start = time.time()
            evalAB, moves = AlphaBeta.alpha_beta_simple(i, board, True)
            end = time.time()
            timetaken = (end - start)
            print("eval:", evalAB)
            print("time:", timetaken)
            # moves.printMove()
            AB_List[i-1] = AB_List[i-1] + timetaken

            print("")
            print("Alpha-Beta_TT")
            start = time.time()
            eval, move = AB.alpha_beta_TT_simple(i, board, True)
            end = time.time()
            timetaken = (end - start)
            print("eval:", eval)
            print("time:", timetaken)
            # move.printMove()
            AB_TT_store_List[i - 1] = AB_TT_store_List[i - 1] + timetaken

            print("")
            print("MTD(f) with f=bestGuess")
            start = time.time()
            evalMTD, movesMTD = MTD.MTDF(evalMTD, i, board, True, 1)
            end = time.time()
            timetaken = (end - start)
            print("eval:", evalMTD)
            print("time:", timetaken)
            #MTD_List.append(timetaken)
            MTD_List[i - 1] = MTD_List[i - 1] + timetaken
            print("----------------------------------")
        print("Iteration",i2,"completed")
        print("----------------------------------")
    print("Benchmark complete")

    for i in range(0, Depth-1):
        AB_List[i] = AB_List[i] / Iterations
        AB_TT_store_List[i] = AB_TT_store_List[i] / Iterations
        MTD_List[i] = MTD_List[i] / Iterations

    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    plt.plot(x, AB_List, label='Alpha-Beta')
    plt.plot(x, AB_TT_store_List, label='Alpha-Beta TT', linestyle='dashed')
    plt.plot(x, MTD_List, label='MTD', linestyle='dashdot')
    plt.xlabel("Depth")
    plt.ylabel("Time taken")
    plt.title("Benchmark Randomboard")
    plt.legend()
    plt.savefig(f"../Resources/Benchmark_Random_Iter_{Iterations}.png")
    plt.show()

def MateIn3_AB():
    board = LionBoard.LionBoard()
    board.setBoard_start()

    #board.setBoard_Fen("eg1/lc1/1CL/G1E/")
    """best move is 3 to 6"""
    #board.setBoard_Fen("eg1/1l1/GE1/1L1/cC")
    """Best Move is 5 to 8"""
    board.setBoard_Fen("1l1/G2/L1g/2E/cCE")
    """Best Move is 8 to 7"""

    board.printBoard()
    times = []
    for i in range(100):
        starttime = time.time()
        eval, move = AlphaBeta.alpha_beta_simple(5, board, True)
        endtime = time.time()
        # print("eval:", eval)
        times.append(endtime - starttime)
    move.printMove()
    avg = 0
    for i in range(100):
        avg = avg + times[i]
    print("Avg. time =", avg / len(times))

def MateIn3():
    # sys.setrecursionlimit(5000)
    board = LionBoard.LionBoard()
    board.setBoard_start()

    #board.setBoard_Fen("eg1/lc1/1CL/G1E/")
    """best move is 3 to 6"""
    #board.setBoard_Fen("eg1/1l1/GE1/1L1/cC")
    """Best Move is 5 to 8"""
    #board.setBoard_Fen("1l1/G2/L1g/2E/cCE")
    """Best Move is 8 to 7"""
    #board.setBoard_Fen("eg1/lc1/1CL/G1E/")
    """Best Move is 3 to 6"""
    board.setBoard_Fen("1g1/G1l/3/1LE/cC")
    """Best Move is 0 to 4"""
    board.printBoard()

    print("AB:")
    eval, move = AlphaBeta.alpha_beta_simple(5, board, True)
    optimalMove = move
    move.printMove()

    Test_MCTS = True
    Test_MCTS_MR = True
    Test_MCTS_MB = True
    Test_MCTS_MS = True
    MCTS_passed_time = 0
    MCTS_MR_passed_time = 0
    MCTS_MB_passed_time = 0
    MCTS_MS_passed_time = 0
    time_iter = 0.1
    Iterations = 50
    Interval = 100
    print("MCTS Test")
    for i in range(Interval):
        print("----------------------------------------")
        print("Time:", (i+1) * time_iter)
        if Test_MCTS:
            print("MCTS")
            Movelist = []
            AllMovesAreSame = True
            for i2 in range(Iterations):
                result_node = MCTS_Solvers.MCTS_Solver_Run(board, True, (i+1) * time_iter)
                Movelist.append(result_node.move)
                #result_node.move.printMove()
            for move in Movelist:
                if not move.equals(optimalMove):
                    AllMovesAreSame = False
            if AllMovesAreSame:
                print("Test passed at", (i+1) * time_iter)
                MCTS_passed_time = (i+1) * time_iter
                Test_MCTS = False
            else:
                print("Test Failed")

        if Test_MCTS_MS:
            print("MCTS-MS")
            Movelist = []
            AllMovesAreSame = True
            for i2 in range(Iterations):
                result_node = MCTS_Solvers.MCTS_MS_Run(board, True, (i+1) * time_iter, 1,4)
                Movelist.append(result_node.move)
                #result_node.move.printMove()
            for move in Movelist:
                if not move.equals(optimalMove):
                    AllMovesAreSame = False
            if AllMovesAreSame:
                print("Test passed at", (i+1) * time_iter)
                MCTS_MS_passed_time = (i + 1) * time_iter
                Test_MCTS_MS = False
            else:
                print("Test Failed")

        if Test_MCTS_MR:
            print("MCTS-MR")
            Movelist = []
            AllMovesAreSame = True
            for i2 in range(Iterations):
                result_node = MCTS_Solvers.MCTS_MR_Run(board, True, (i+1) * time_iter, 1)
                Movelist.append(result_node.move)
                #result_node.move.printMove()
            for move in Movelist:
                if not move.equals(optimalMove):
                    AllMovesAreSame = False
            if AllMovesAreSame:
                print("Test passed at", (i+1) * time_iter)
                MCTS_MR_passed_time = (i + 1) * time_iter
                Test_MCTS_MR = False
            else:
                print("Test Failed")

        if Test_MCTS_MB:
            print("MCTS-MB")
            Movelist = []
            AllMovesAreSame = True
            for i2 in range(Iterations):
                result_node = MCTS_Solvers.MCTS_MB_Run(board, True, (i+1) * time_iter, 3)
                Movelist.append(result_node.move)
                #result_node.move.printMove()
            for move in Movelist:
                if not move.equals(optimalMove):
                    AllMovesAreSame = False
            if AllMovesAreSame:
                print("Test passed at", (i+1) * time_iter)
                MCTS_MB_passed_time = (i + 1) * time_iter
                Test_MCTS_MB = False
            else:
                print("Test Failed")

        if not Test_MCTS and not Test_MCTS_MS and not Test_MCTS_MR and not Test_MCTS_MB:
            break

    print("Results:")
    print("MCTS passed at:", MCTS_passed_time)
    print("MCTS-MR passed at:", MCTS_MR_passed_time)
    print("MCTS-MB passed at:", MCTS_MB_passed_time)
    print("MCTS-MS passed at:", MCTS_MS_passed_time)

if __name__ == '__main__':
    #TestPostion()
    #Testing_PV()
    #MateIn3()
    #MateIn3_AB()
    #Mate_in_Benchmark()
    #Random_Benchmark()
    AB_VS_AB()