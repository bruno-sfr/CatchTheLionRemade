import sys
import time

from AlphaBeta import AlphaBeta, IterativeDeepening
from Game import LionBoard
from pathlib import Path

Positions = ["elg/1c1/1C1/GLE/", "elg/1c1/1CL/G1E/", "elg/1c1/LC1/G1E/", "elg/1c1/GC1/1LE/", "elg/1C1/111/GLE/C",
             "e1g/lc1/1CL/G1E/", "el1/1cg/1CL/G1E/", "elg/111/1cL/G1E/c", "e1g/1cl/LC1/G1E/", "el1/1cg/LC1/G1E/",
             "elg/111/Lc1/G1E/c", "e1g/1cl/GC1/1LE/", "el1/1cg/GC1/1LE/", "elg/111/Gc1/1LE/c", "e1g/1Cl/111/GLE/C",
             "e1g/1l1/111/GLE/cC", "e1g/lC1/111/GLE/C", "1lg/1e1/111/GLE/cC"]

WhiteTurns = [True, False, False, False, False,
              True, True, True, True, True,
              True, True, True, True, True,
              True, True, True]

if len(sys.argv) != 4:
    print("Missing Arguments, expected are in that order:")
    print("Time A_player B_player")
    exit()

Time = int(sys.argv[1])
A_player = str(sys.argv[2])
B_player = str(sys.argv[3])

max_turns = 100

A_Wins = 0
B_Wins = 0
A_Depths = []
B_Depths = []
for i_pos in range(len(Positions)):
    for i in range(2):
        ID_white = IterativeDeepening.iterativeDeepeningAB()
        ID_MTD_white = IterativeDeepening.iterativeDeepeningMTD()
        ID_black = IterativeDeepening.iterativeDeepeningAB()
        ID_MTD_black = IterativeDeepening.iterativeDeepeningMTD()
        board = LionBoard.LionBoard()
        board.setBoard_Fen(Positions[i_pos])
        whiteTurn = WhiteTurns[i_pos]
        turns = 0
        if i == 0:
            #print("Even Play")
            while not board.isGameOver():
                depth = 0
                if whiteTurn:
                    match A_player:
                        case "MiniMax":
                            evalAB, move, depth = ID_white.iterativeDeepening_MM(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBeta":
                            evalAB, move, depth = ID_white.iterativeDeepening_AB(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBetaQuiet":
                            evalAB, move, depth = ID_white.iterativeDeepening_AB_Q(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBetaTT":
                            evalAB, move, depth = ID_white.iterativeDeepening_AB_TT(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "MTD":
                            evalAB, move, depth = ID_MTD_white.iterativeDeepening_MTD(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    if depth < 20:
                        A_Depths.append(depth)
                    print(f"{A_player}-Depth: {depth}")
                else:
                    match B_player:
                        case "MiniMax":
                            evalAB, move, depth = ID_black.iterativeDeepening_MM(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBeta":
                            evalAB, move, depth = ID_black.iterativeDeepening_AB(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBetaQuiet":
                            evalAB, move, depth = ID_black.iterativeDeepening_AB_Q(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBetaTT":
                            evalAB, move, depth = ID_black.iterativeDeepening_AB_TT(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "MTD":
                            evalAB, move, depth = ID_MTD_black.iterativeDeepening_MTD(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    if depth < 20:
                        B_Depths.append(depth)
                    print(f"{B_player}-Depth: {depth}")
                whiteTurn = not whiteTurn
                turns = turns + 1
                if turns > max_turns:
                    break

            if board.hasWhiteWon():
                A_Wins = A_Wins + 1
            elif board.hasBlackWon():
                B_Wins = B_Wins + 1
            else:
                B_Wins = B_Wins + 0.5
                A_Wins = A_Wins + 0.5
        else:
            #print("Uneven Play")
            while not board.isGameOver():
                depth = 0
                if whiteTurn:
                    match B_player:
                        case "MiniMax":
                            evalAB, move, depth = ID_white.iterativeDeepening_MM(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBeta":
                            evalAB, move, depth = ID_white.iterativeDeepening_AB(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBetaQuiet":
                            evalAB, move, depth = ID_white.iterativeDeepening_AB_Q(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBetaTT":
                            evalAB, move, depth = ID_white.iterativeDeepening_AB_TT(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "MTD":
                            evalAB, move, depth = ID_MTD_white.iterativeDeepening_MTD(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    if depth < 20:
                        B_Depths.append(depth)
                    print(f"{B_player}-Depth: {depth}")
                else:
                    match A_player:
                        case "MiniMax":
                            evalAB, move, depth = ID_black.iterativeDeepening_MM(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBeta":
                            evalAB, move, depth = ID_black.iterativeDeepening_AB(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBetaQuiet":
                            evalAB, move, depth = ID_black.iterativeDeepening_AB_Q(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "AlphaBetaTT":
                            evalAB, move, depth = ID_black.iterativeDeepening_AB_TT(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                        case "MTD":
                            evalAB, move, depth = ID_MTD_black.iterativeDeepening_MTD(Time, board, whiteTurn)
                            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    if depth < 20:
                        A_Depths.append(depth)
                    print(f"{A_player}-Depth: {depth}")
                whiteTurn = not whiteTurn
                turns = turns + 1
                if turns > max_turns:
                    break

            if board.hasWhiteWon():
                B_Wins = B_Wins + 1
            elif board.hasBlackWon():
                A_Wins = A_Wins + 1
            else:
                B_Wins = B_Wins + 0.5
                A_Wins = A_Wins + 0.5
    print(f"{A_player} {A_Wins} : {B_Wins} {B_player}")

A_Depth_avg = 0
for i in A_Depths:
    A_Depth_avg = A_Depth_avg + i
A_Depth_avg = A_Depth_avg / len(A_Depths)

B_Depth_avg = 0
for i in B_Depths:
    B_Depth_avg = B_Depth_avg + i
B_Depth_avg = B_Depth_avg / len(B_Depths)

Path(f"./Resources/ID_{A_player}-vs-{B_player}/Time-{Time}s").mkdir(parents=True, exist_ok=True)
with open(f'./Resources/ID_{A_player}-vs-{B_player}/Time-{Time}s/{time.time()}.txt', 'a') as the_file:
    the_file.write(f"{A_player} {A_Wins}:{B_Wins} {B_player}\n")
    the_file.write(f"Depths AVG: {A_player} {A_Depth_avg}:{B_Depth_avg} {B_player}\n")
