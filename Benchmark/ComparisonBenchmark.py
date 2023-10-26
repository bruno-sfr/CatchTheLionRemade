import math
import sys

import matplotlib.pyplot as plt

from Game import LionBoard, Move
from AlphaBeta import IterativeDeepening
from AlphaBeta import AlphaBeta
from MonteCarlo import MCTS


def ABvsABTT_fixedDepth():
    AB_wins = 0
    ABTT_wins = 0
    AB_wins_List = []
    ABTT_wins_List = []
    #RoundCounts = []
    Depth = 7
    for i in range(0, 15):
        board = LionBoard.LionBoard()
        board.setBoard_start()
        AB_TT = AlphaBeta.Alpha_Beta_TranspostionTable()
        if i < 5:
            whiteTurn = True
        else:
            whiteTurn = False
        #roundcount = 0
        while not board.isGameOver():
            print("---")
            board.printBoard()
            if whiteTurn:
                print("Alpha-Beta")
                eval, moves = AlphaBeta.alpha_beta_simple(Depth, board, whiteTurn)
                if len(moves) == 0:
                    print("no move Returned")
                # _from = moves[0].getFrom
                # _tp = moves[0].getTo
                #moves[0].printMove()
                print("Making Move:", board.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo()))
            else:
                print("Alpha-Beta TT")
                eval, moves = AB_TT.alpha_beta_TT_simple(Depth, board, whiteTurn)
                if len(moves) == 0:
                    print("no move Returned")
                # _from = moves[0].getFrom
                # _tp = moves[0].getTo
                #moves[0].printMove()
                print("Making Move:", board.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo()))
            whiteTurn = not whiteTurn
            #roundcount = roundcount + 1
        #RoundCounts.append(roundcount)
        if board.hasWhiteWon():
            AB_wins = AB_wins + 1
        elif board.hasBlackWon():
            ABTT_wins = ABTT_wins + 1
        print("--------------------")
        print("AB:", AB_wins)
        print("ABTT:", ABTT_wins)
        print("--------------------")
        AB_wins_List.append(AB_wins)
        ABTT_wins_List.append(ABTT_wins)
        #board.printBoard()
    x = range(0, 15)
    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    plt.plot(x, AB_wins_List, label='Alpha-Beta')
    plt.plot(x, ABTT_wins_List, label='Alpha-Beta TT')
    plt.xlabel("Rounds")
    plt.ylabel("Wins")
    plt.title("Comparison AB vs ABTT Fixed Depth=7")
    plt.legend()
    #plt.savefig("./Benchmark/Benchmark_ABvsABTT_FixedDepth.png")
    plt.savefig("../Resources/Benchmark_ABvsABTT_FixedDepth.png")
    plt.show()

def ABvsABTT_iterativeDeepening():
    AB_wins = 0
    ABTT_wins = 0
    AB_wins_List = []
    ABTT_wins_List = []
    time = 20
    for i in range(0, 10):
        board = LionBoard.LionBoard()
        board.setBoard_start()
        ID = IterativeDeepening.iterativeDeepeningAB()
        if i % 2 == 0:
            whiteTurn = True
        else:
            whiteTurn = False
        while not board.isGameOver():
            # board.printBoard()
            if whiteTurn:
                print("Alpha-Beta")
                eval, moves = ID.iterativeDeepening_AB(time, board, whiteTurn)
                if len(moves) == 0:
                    print("no move Returned")
                # _from = moves[0].getFrom
                # _tp = moves[0].getTo
                moves[0].printMove()
                print("Making Move:", board.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo()))
            else:
                print("Alpha-Beta TT")
                eval, moves = ID.iterativeDeepening_AB_TT(time, board, whiteTurn)
                if len(moves) == 0:
                    print("no move Returned")
                # _from = moves[0].getFrom
                # _tp = moves[0].getTo
                moves[0].printMove()
                print("Making Move:", board.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo()))
            whiteTurn = not whiteTurn
        if board.hasWhiteWon():
            AB_wins = AB_wins + 1
        elif board.hasBlackWon():
            ABTT_wins = ABTT_wins + 1
        print("--------------------")
        print("AB:", AB_wins)
        print("ABTT:", ABTT_wins)
        print("--------------------")
        AB_wins_List.append(AB_wins)
        ABTT_wins_List.append(ABTT_wins)
        # board.printBoard()
    x = range(0, 10)
    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    plt.plot(x, AB_wins_List, label='Alpha-Beta')
    plt.plot(x, ABTT_wins_List, label='Alpha-Beta TT')
    plt.xlabel("Rounds")
    plt.ylabel("Wins")
    plt.title("Comparison ID AB vs ABTT Time 20s")
    plt.legend()
    plt.savefig("../Resources/Benchmark_ABvsABTT_Iterative_Deepening_20s.png")
    plt.show()

def ABvsMCTS():
    AB_wins = 0
    MCTS_wins = 0
    AB_wins_List = [0]
    MCTS_wins_List = [0]
    time = 10
    Iterations = 10
    for i in range(0, Iterations):
        board = LionBoard.LionBoard()
        board.setBoard_start()
        ID = IterativeDeepening.iterativeDeepeningAB()
        if i % 2 == 0:
            whiteTurn = True
        else:
            whiteTurn = False
        while not board.isGameOver():
            # board.printBoard()
            if whiteTurn:
                print("Alpha-Beta")
                eval, moves = ID.iterativeDeepening_AB_TT(time, board, whiteTurn)
                if len(moves) == 0:
                    print("no move Returned")
                # _from = moves[0].getFrom
                # _tp = moves[0].getTo
                moves[0].printMove()
                print("Making Move:", board.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo()))
            else:
                print("MCTS")
                ResultNode = MCTS.MCTS(board, whiteTurn, time)
                if len(moves) == 0:
                    print("no move Returned")
                # _from = moves[0].getFrom
                # _tp = moves[0].getTo
                ResultNode.move.printMove()
                print("Making Move:", board.makeMove(whiteTurn, ResultNode.move.getFrom(), ResultNode.move.getTo()))
            whiteTurn = not whiteTurn
        if board.hasWhiteWon():
            AB_wins = AB_wins + 1
        elif board.hasBlackWon():
            MCTS_wins = MCTS_wins + 1
        print("--------------------")
        print("AB:", AB_wins)
        print("MCTS:", MCTS_wins)
        print("--------------------")
        AB_wins_List.append(AB_wins)
        MCTS_wins_List.append(MCTS_wins)
        # board.printBoard()
    x = range(0, Iterations+1)
    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    plt.plot(x, AB_wins_List, label='Alpha-Beta')
    plt.plot(x, MCTS_wins_List, label='MCTS')
    plt.xlabel("Rounds")
    plt.ylabel("Wins")
    plt.title("Comparison ID AB vs MCTS Time 10s")
    plt.legend()
    plt.savefig("../Resources/Benchmark_ABvsMCTS_Iterative_Deepening_10s.png")
    plt.show()

def MCTSvsMCTS_FE():
    MCTS_FE_wins = 0
    MCTS_wins = 0
    MCTS_FE_wins_List = [0]
    MCTS_wins_List = [0]
    time = 15
    Iterations = 5
    for i in range(0, Iterations):
        board = LionBoard.LionBoard()
        board.setBoard_start()
        if i % 2 == 0:
            whiteTurn = True
        else:
            whiteTurn = False
        while not board.isGameOver():
            # board.printBoard()
            if whiteTurn:
                print("MCTS Full Expansion")
                ResultNode = MCTS.MCTS_full_expansion(board, whiteTurn, time)
                ResultNode.move.printMove()
                print("Making Move:", board.makeMove(whiteTurn, ResultNode.move.getFrom(), ResultNode.move.getTo()))
            else:
                print("MCTS")
                ResultNode = MCTS.MCTS(board, whiteTurn, time)
                ResultNode.move.printMove()
                print("Making Move:", board.makeMove(whiteTurn, ResultNode.move.getFrom(), ResultNode.move.getTo()))
            whiteTurn = not whiteTurn
        if board.hasWhiteWon():
            MCTS_FE_wins = MCTS_FE_wins + 1
        elif board.hasBlackWon():
            MCTS_wins = MCTS_wins + 1
        print("--------------------")
        print("MCTS_FE:", MCTS_FE_wins)
        print("MCTS:", MCTS_wins)
        print("--------------------")
        MCTS_FE_wins_List.append(MCTS_FE_wins)
        MCTS_wins_List.append(MCTS_wins)
        # board.printBoard()
    x = range(0, Iterations+1)
    x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
    plt.xticks(x_list)

    plt.plot(x, MCTS_FE_wins_List, label='MCTS_FE')
    plt.plot(x, MCTS_wins_List, label='MCTS')
    plt.xlabel("Rounds")
    plt.ylabel("Wins")
    plt.title("Comparison MCTS_FE vs MCTS Time 10s")
    plt.legend()
    plt.savefig("../Resources/Benchmark_MCTSFEvsMCTS_Iterative_Deepening_10s_dummy.png")
    plt.show()

if __name__ == '__main__':
    sys.setrecursionlimit(15000)
    #ABvsABTT_fixedDepth()
    #ABvsABTT_iterativeDeepening()
    #ABvsMCTS()
    MCTSvsMCTS_FE()
