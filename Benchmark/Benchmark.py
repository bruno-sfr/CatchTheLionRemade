import math
import time

import matplotlib.pyplot as plt

from AlphaBeta import AlphaBeta
from Game import LionBoard
from MonteCarlo import MCTS_Solvers


def TestStartpostion():
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

    AB_Final = AlphaBeta.Alpha_Beta_TT_Final()
    MTD_second_guess = AlphaBeta.MTDF()

    Depth = 10
    x = range(1, Depth)

    for i in range(1, Depth):
        print("Depth:", i)
        print("MiniMax")
        start = time.time()
        evalMM, moves = AlphaBeta.MiniMax(i, board, whiteTurn, [])
        end = time.time()
        timetaken = (end - start)
        print("eval:", evalMM)
        print("time:", timetaken)
        moves.printMove()
        MM_List.append(timetaken)
        MM_Eval_List.append(evalMM)

        print("Depth:", i)
        print("Alpha-Beta")
        start = time.time()
        evalAB, moves = AlphaBeta.alpha_beta_simple(i, board, whiteTurn)
        end = time.time()
        timetaken = (end - start)
        print("eval:", evalAB)
        print("time:", timetaken)
        moves.printMove()
        AB_List.append(timetaken)
        AB_Eval_List.append(evalAB)

        print("")
        print("Alpha-Beta_TT_final")
        start = time.time()
        eval, move = AB_Final.alpha_beta_TT_final(float('-inf'), float('inf'), i, board, whiteTurn, True)
        end = time.time()
        timetaken = (end - start)
        print("eval:", eval)
        print("time:", timetaken)
        move.printMove()
        AB_TT_store_List.append(timetaken)
        AB_TT_store_Eval_List.append(eval)

        print("")
        print("MTD(f) with f=bestSecondGuess")
        start = time.time()
        if i % 2 == 0:
            print("Run Even")
            evalMTD_even, movesMTD = MTD_second_guess.MTDF(evalMTD_even, i, board, whiteTurn, 0.1)
        else:
            print("Run Uneven")
            evalMTD_uneven, movesMTD = MTD_second_guess.MTDF(evalMTD_uneven, i, board, whiteTurn, 0.1)
        end = time.time()
        timetaken = (end - start)
        if i % 2 == 0:
            print("eval:", evalMTD_even)
            MTD_second_guess_Eval_List.append(evalMTD_even)
        else:
            print("eval:", evalMTD_uneven)
            MTD_second_guess_Eval_List.append(evalMTD_uneven)
        print("time:", timetaken)
        movesMTD.printMove()
        MTD_second_guess_List.append(timetaken)
        print("----------------------------------")
    print("Benchmark complete")

    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    plt.plot(x, MM_List, label='MiniMax')
    plt.plot(x, AB_List, label='Alpha-Beta')
    plt.plot(x, AB_TT_store_List, label='Alpha-Beta TT', linestyle='dotted')
    plt.plot(x, MTD_second_guess_List, label='MTD(f)', linestyle='dashed')
    plt.legend(loc='upper left')

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

    plt.xlabel("Depth")
    plt.ylabel("Time taken")
    plt.title("Benchmark")
    plt.savefig(f"../Resources/Benchmark_Start_Depth_{Depth}.png")
    plt.show()

def Random_Benchmark():
    board = LionBoard.LionBoard()
    #board.randomBoard()
    #board.printBoard()

    Depth = 8
    Iterations = 5

    AB_List = [0] * (Depth - 1)
    AB_TT_List = [0] * (Depth - 1)
    MTD_List = [0] * (Depth - 1)
    AB_TT_store_List = [0] * (Depth - 1)
    MTD_no_TT_List = [0] * (Depth - 1)
    #MTD_0_List = []
    x = range(1, Depth)

    for i2 in range(0, Iterations):
        board.randomBoard()
        MTD = AlphaBeta.MTDF()
        MTD_0 = AlphaBeta.MTDF()
        MTD_no_TT = AlphaBeta.MTDF()
        AB = AlphaBeta.Alpha_Beta_TranspostionTable()
        AB_store = AlphaBeta.Alpha_Beta_TranspostionTable()

        evalMTD = 0.0
        evalMTD_no_tt = 0.0
        for i in range(1, Depth):
            print("Depth:", i)
            print("Alpha-Beta")
            start = time.time()
            eval, moves = AlphaBeta.alpha_beta_simple(i, board, True)
            end = time.time()
            timetaken = (end - start)
            print("eval:", eval)
            print("time:", timetaken)
            for move in moves:
                move.printMove()
                break
            AB_List[i-1] = AB_List[i-1] + timetaken

            """print("")
            print("Alpha-Beta_TT")
            start = time.time()
            eval, moves = AB.alpha_beta_TT(float('-inf'), float('inf'), i, board, True, [], False)
            end = time.time()
            timetaken = (end - start)
            print("eval:", eval)
            print("time:", timetaken)
            for move in moves:
                move.printMove()
                break
            #AB_TT_List.append(timetaken)
            AB_TT_List[i - 1] = AB_TT_List[i - 1] + timetaken"""

            print("")
            print("Alpha-Beta_TT_store_All")
            start = time.time()
            # eval, moves = AB.alpha_beta_TT_simple(i, board, True)
            eval, moves = AB_store.alpha_beta_TT(float('-inf'), float('inf'), i, board, True, [], True)
            end = time.time()
            timetaken = (end - start)
            print("eval:", eval)
            print("time:", timetaken)
            for move in moves:
                move.printMove()
                break
            #AB_TT_store_List.append(timetaken)
            AB_TT_store_List[i - 1] = AB_TT_store_List[i - 1] + timetaken

            print("")
            print("MTD(f) with f=bestGuess")
            start = time.time()
            evalMTD, movesMTD = MTD.MTDF(evalMTD, i, board, True, 1)
            end = time.time()
            timetaken = (end - start)
            print("eval:", evalMTD)
            print("time:", timetaken)
            if len(movesMTD) == 0:
                print("No Move found")
            for move in movesMTD:
                move.printMove()
                break
            #MTD_List.append(timetaken)
            MTD_List[i - 1] = MTD_List[i - 1] + timetaken

            """
            print("")
            print("MTD(f) with f=0")
            start = time.time()
            evalMTD_0, movesMTD_0 = MTD_0.MTDF(0, i, board, True)
            end = time.time()
            timetaken = (end - start)
            print("eval:", evalMTD_0)
            print("time:", timetaken)
            if len(movesMTD_0) == 0:
                print("No Move found")
            for move in movesMTD_0:
                move.printMove()
                break
            MTD_0_List.append(timetaken)"""

            """print("")
            print("MTD(f) with no TT")
            start = time.time()
            evalMTD_no_tt, movesMTD_no_tt = MTD_no_TT.MTDF_no_TT(0, i, board, True, 0.1)
            end = time.time()
            timetaken = (end - start)
            print("eval:", evalMTD_no_tt)
            print("time:", timetaken)
            print("tt use", MTD_no_TT.count_transpo)
            if len(movesMTD_no_tt) == 0:
                print("No Move found")
            for move in movesMTD_no_tt:
                move.printMove()
                break
            MTD_no_TT_List[i - 1] = MTD_no_TT_List[i - 1] + timetaken"""
            print("----------------------------------")
        print("Iteration",i2,"completed")
        print("----------------------------------")
    print("Benchmark complete")

    for i in range(0, Depth-1):
        AB_List[i] = AB_List[i] / Iterations
        AB_TT_List[i] = AB_TT_List[i] / Iterations
        AB_TT_store_List[i] = AB_TT_store_List[i] / Iterations
        MTD_List[i] = MTD_List[i] / Iterations
        MTD_no_TT_List[i] = MTD_no_TT_List[i] / Iterations

    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    plt.plot(x, AB_List, label='Alpha-Beta')
    #plt.plot(x, AB_TT_List, label='Alpha-Beta TT', linestyle='dotted')
    plt.plot(x, AB_TT_store_List, label='Alpha-Beta TT Store All', linestyle='dashed')
    plt.plot(x, MTD_List, label='MTD(f) with f = best guess', linestyle='dashdot')
    #plt.plot(x, MTD_no_TT_List, label='MTD(f) with no TT', linestyle='dotted')
    #plt.plot(x, MTD_0_List, label='MTD(f) with f = 0')
    plt.xlabel("Depth")
    plt.ylabel("Time taken")
    plt.title("Benchmark Randomboard")
    plt.legend()
    plt.savefig(".../Resources/Benchmark_Random_Iter_15.png")
    plt.show()

def MateIn3_AB():
    board = LionBoard.LionBoard()
    board.setBoard_start()

    board.setBoard_Fen("eg1/lc1/1CL/G1E/")
    """best move is 3 to 6"""
    #board.setBoard_Fen("eg1/1l1/GE1/1L1/cC")
    """Best Move is 5 to 8"""

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
    board.setBoard_Fen("eg1/1l1/GE1/1L1/cC")
    """Best Move is 5 to 8"""

    print("AB:")
    eval, move = AlphaBeta.alpha_beta_simple(5, board, True)
    optimalMove = move
    move.printMove()

    Test_MCTS = False
    Test_MCTS_MR = False
    Test_MCTS_MB = False
    Test_MCTS_MS = False
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
        print("Time:", (i+1) * time_iter + 1)
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
    #TestStartpostion()
    #MateIn3()
    MateIn3_AB()
    #Random_Benchmark()