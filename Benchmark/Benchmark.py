import math
import time

import matplotlib.pyplot as plt

from AlphaBeta import AlphaBeta
from Game import LionBoard
from MTDF import MTDF


def TestStartpostion():
    board = LionBoard.LionBoard()
    board.setBoard_start()
    """MTD = MTDF.MTDF()
    MTD_MiniMax = MTDF.MTDF()
    MTD_0 = MTDF.MTDF()"""
    #AB = AlphaBeta.Alpha_Beta_TranspostionTable()
    #AB_store = AlphaBeta.Alpha_Beta_TranspostionTable()
    evalMTD = 0.0

    AB_List = []
    AB_TT_List = []
    AB_TT_store_List = []
    MTD_List = []
    MTD_0_List = []
    MTD_MiniMax_List = []
    MTD_no_TT_List = []

    AB_Eval_List = []
    AB_TT_Eval_List = []
    AB_TT_store_Eval_List = []
    MTD_Eval_List = []
    MTD_0_Eval_List = []
    MTD_MiniMax_Eval_List = []
    MTD_no_TT_Eval_List = []

    Depth = 10
    x = range(1, Depth)

    for i in range(1, Depth):
        AB = AlphaBeta.Alpha_Beta_TranspostionTable()
        AB_store = AlphaBeta.Alpha_Beta_TranspostionTable()
        MTD = MTDF.MTDF()
        MTD_MiniMax = MTDF.MTDF()
        MTD_0 = MTDF.MTDF()
        MTD_no_TT = MTDF.MTDF()

        print("Depth:", i)
        print("Alpha-Beta")
        start = time.time()
        evalAB, moves = AlphaBeta.alpha_beta_simple(i, board, True)
        end = time.time()
        timetaken = (end - start)
        print("eval:", evalAB)
        print("time:", timetaken)
        for move in moves:
            move.printMove()
            break
        AB_List.append(timetaken)
        AB_Eval_List.append(evalAB)

        print("")
        print("Alpha-Beta_TT")
        start = time.time()
        #eval, moves = AB.alpha_beta_TT_simple(i, board, True)
        eval, moves = AB.alpha_beta_TT(float('-inf'), float('inf'), i, board, True, [], False)
        end = time.time()
        timetaken = (end - start)
        print("eval:", eval)
        print("time:", timetaken)
        for move in moves:
            move.printMove()
            break
        AB_TT_List.append(timetaken)
        AB_TT_Eval_List.append(eval)

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
        AB_TT_store_List.append(timetaken)
        AB_TT_store_Eval_List.append(eval)

        #print("----------------------------------")

        """print("")
        print("MTD(f) with f=bestGuess")
        start = time.time()
        evalMTD, movesMTD = MTD.MTDF(evalMTD, i, board, True, 0.1)
        end = time.time()
        timetaken = (end - start)
        print("eval:", evalMTD)
        print("time:", timetaken)
        if len(movesMTD) == 0:
            print("No Move found")
        for move in movesMTD:
            move.printMove()
            break
        MTD_List.append(timetaken)
        MTD_Eval_List.append(evalMTD)

        print("")
        print("MTD(f) with f=BestMiniMax")
        start = time.time()
        eval, moves = MTD_MiniMax.MTDF(evalAB, i, board, True, 0.1)
        end = time.time()
        timetaken = (end - start)
        print("eval:", eval)
        print("time:", timetaken)
        if len(moves) == 0:
            print("No Move found")
        for move in moves:
            move.printMove()
            break
        MTD_MiniMax_List.append(timetaken)
        MTD_MiniMax_Eval_List.append(eval)"""

        print("")
        print("MTD(f) with f=0")
        start = time.time()
        evalMTD_0, movesMTD_0 = MTD_0.MTDF(0, i, board, True, 0.1)
        end = time.time()
        timetaken = (end - start)
        print("eval:", evalMTD_0)
        print("time:", timetaken)
        print("tt use", MTD_0.count_transpo)
        if len(movesMTD_0) == 0:
            print("No Move found")
        for move in movesMTD_0:
            move.printMove()
            break
        MTD_0_List.append(timetaken)
        MTD_0_Eval_List.append(evalMTD_0)

        print("")
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
        MTD_no_TT_List.append(timetaken)
        MTD_no_TT_Eval_List.append(evalMTD_no_tt)
        print("----------------------------------")
    print("Benchmark complete")

    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    fig, axs = plt.subplots(2, sharex=True)
    fig.suptitle("Comparison")

    axs[0].plot(x, AB_List, label='Alpha-Beta')
    #axs[0].plot(x, AB_TT_List, label='Alpha-Beta TT', linestyle='dotted')
    axs[0].plot(x, AB_TT_store_List, label='Alpha-Beta TT Store All', linestyle='dashed')
    #axs[0].plot(x, MTD_List, label='MTD(f) with f = best guess', linestyle='dashed')
    #axs[0].plot(x, MTD_MiniMax_List, label='MTD(f) with f = BestMiniMax', linestyle='dashdot')
    axs[0].plot(x, MTD_0_List, label='MTD(f) with f = 0')
    axs[0].plot(x, MTD_no_TT_List, label='MTD(f) with no TT')
    axs[0].set(ylabel='Time taken')

    axs[0].legend(loc='upper left')

    axs[1].plot(x, AB_Eval_List, label='Alpha-Beta')
    #axs[1].plot(x, AB_TT_Eval_List, label='Alpha-Beta TT', linestyle='dotted')
    axs[1].plot(x, AB_TT_store_Eval_List, label='Alpha-Beta TT Store All', linestyle='dashed')
    #axs[1].plot(x, MTD_Eval_List, label='MTD(f) with f = best guess', linestyle='dashed')
    #axs[1].plot(x, MTD_MiniMax_Eval_List, label='MTD(f) with f = BestMiniMax', linestyle='dashdot')
    axs[1].plot(x, MTD_0_Eval_List, label='MTD(f) with f = 0')
    axs[1].plot(x, MTD_no_TT_Eval_List, label='MTD(f) with no TT')
    axs[1].set(ylabel='Eval')

    """plt.plot(x, AB_List, label='Alpha-Beta')
    plt.plot(x, AB_TT_List, label='Alpha-Beta TT')
    plt.plot(x, MTD_List, label='MTD(f) with f = best guess')
    plt.plot(x, MTD_MiniMax_List, label='MTD(f) with f = BestMiniMax')
    plt.plot(x, MTD_0_List, label='MTD(f) with f = 0')"""
    #axs[0].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncols=2, mode="expand", borderaxespad=0.)
    plt.xlabel("Depth")
    #plt.ylabel("Time taken")
    #plt.title("Benchmark")
    plt.savefig("../Resources/Benchmark_Start_Depth_4.png")
    plt.show()

def MTD_Increment_Comparison():
    board = LionBoard.LionBoard()
    #board.setBoard_start()
    board.randomBoard()
    DiffList = []

    print("Alpha-Beta")
    evalAB, moves = AlphaBeta.alpha_beta_simple(8, board, True)
    print("eval:", evalAB)
    for move in moves:
        move.printMove()
        break

    print("----------------------------------")
    increment = 0.0000000001
    increment_list = []
    time_list = []
    for i in range(1, 20):
        MTD = MTDF.MTDF()
        increment_list.append(increment)
        print("Increment:", increment)
        start = time.time()
        evalMTD, movesMTD = MTD.MTDF(evalAB, 7, board, True, increment)
        end = time.time()
        timetaken = (end - start)
        time_list.append(timetaken)
        print("eval:", evalMTD)
        print("time:", timetaken)
        if len(movesMTD) == 0:
            print("No Move found")
        for move in movesMTD:
            move.printMove()
            break
        Diffrence = abs(evalAB - evalMTD)
        print("Diffrence:", Diffrence)
        DiffList.append(Diffrence)
        increment = increment * 10
    print("----------------------------------")

    #x = range(1, 20)
    #x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    #plt.xticks(x_list)

    #plt.plot(increment_list, DiffList, label='Diffrence')
    plt.semilogx(increment_list, DiffList, label='Diffrence')
    plt.semilogx(increment_list, time_list, label='Time')
    plt.xlabel("Increment")
    plt.ylabel("Diffrence")
    plt.title("Benchmark Increment")
    plt.legend()
    plt.savefig("../Resources/Benchmark_Increment_3.png")
    plt.show()

def MateIn1():
    board = LionBoard.LionBoard()
    #board.setBoard_Fen("2l/L2/1EC/3/")
    board.setBoard_Fen("G1l/2c/2C/L1G/E")
    board.printBoard()
    MTD = MTDF.MTDF()
    MTD_0 = MTDF.MTDF()
    AB = AlphaBeta.Alpha_Beta_TranspostionTable()
    evalMTD = 0.0

    AB_List = []
    AB_TT_List = []
    MTD_List = []
    MTD_0_List = []
    Depth = 8
    x = range(1, Depth)

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
        AB_List.append(timetaken)

        print("")
        print("Alpha-Beta_TT")
        start = time.time()
        eval, moves = AB.alpha_beta_TT_simple(i, board, True)
        end = time.time()
        timetaken = (end - start)
        print("eval:", eval)
        print("time:", timetaken)
        for move in moves:
            move.printMove()
            break
        AB_TT_List.append(timetaken)

        print("")
        print("MTD(f) with f=bestGuess")
        start = time.time()
        evalMTD, movesMTD = MTD.MTDF(evalMTD, i, board, True)
        end = time.time()
        timetaken = (end - start)
        print("eval:", evalMTD)
        print("time:", timetaken)
        if len(movesMTD) == 0:
            print("No Move found")
        for move in movesMTD:
            move.printMove()
            break
        MTD_List.append(timetaken)

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
        MTD_0_List.append(timetaken)
        print("----------------------------------")
    print("Benchmark complete")

    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    plt.plot(x, AB_List, label='Alpha-Beta')
    plt.plot(x, AB_TT_List, label='Alpha-Beta TT')
    plt.plot(x, MTD_List, label='MTD(f) with f = best guess')
    plt.plot(x, MTD_0_List, label='MTD(f) with f = 0')
    plt.xlabel("Depth")
    plt.ylabel("Time taken")
    plt.title("Benchmark")
    plt.legend()
    plt.savefig("../Resources/Benchmark_Mate in few.png")
    plt.show()

def Random_Benchmark():
    board = LionBoard.LionBoard()
    #board.randomBoard()
    #board.printBoard()
    MTD = MTDF.MTDF()
    MTD_0 = MTDF.MTDF()
    AB = AlphaBeta.Alpha_Beta_TranspostionTable()
    AB_store = AlphaBeta.Alpha_Beta_TranspostionTable()
    evalMTD = 0.0

    Depth = 10
    Iterations = 15

    AB_List = [0] * (Depth - 1)
    AB_TT_List = [0] * (Depth - 1)
    MTD_List = [0] * (Depth - 1)
    AB_TT_store_List = [0] * (Depth - 1)
    #MTD_0_List = []
    x = range(1, Depth)

    for i2 in range(0, Iterations):
        board.randomBoard()
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

            print("")
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
            AB_TT_List[i - 1] = AB_TT_List[i - 1] + timetaken

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
            print("----------------------------------")
        print("Iteration",i2,"completed")
        print("----------------------------------")
    print("Benchmark complete")

    for i in range(0, Depth-1):
        AB_List[i] = AB_List[i] / Iterations
        AB_TT_List[i] = AB_TT_List[i] / Iterations
        AB_TT_store_List[i] = AB_TT_store_List[i] / Iterations
        MTD_List[i] = MTD_List[i] / Iterations

    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    plt.plot(x, AB_List, label='Alpha-Beta')
    plt.plot(x, AB_TT_List, label='Alpha-Beta TT', linestyle='dotted')
    plt.plot(x, AB_TT_store_List, label='Alpha-Beta TT Store All', linestyle='dashed')
    plt.plot(x, MTD_List, label='MTD(f) with f = best guess', linestyle='dashdot')
    #plt.plot(x, MTD_0_List, label='MTD(f) with f = 0')
    plt.xlabel("Depth")
    plt.ylabel("Time taken")
    plt.title("Benchmark Randomboard")
    plt.legend()
    plt.savefig(".../Resources/Benchmark_Random_Iter_15.png")
    plt.show()

if __name__ == '__main__':
    TestStartpostion()
    #MTD_Increment_Comparison()
    #MateIn1()
    #Random_Benchmark()