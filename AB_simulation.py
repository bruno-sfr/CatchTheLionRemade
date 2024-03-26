import sys
import time

from AlphaBeta import AlphaBeta
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

if len(sys.argv) != 5:
    print("Missing Arguments, expected are in that order:")
    print("Depth MaxDepth A_player B_player")
    exit()

Depth = int(sys.argv[1])
MaxDepth = int(sys.argv[2])
A_player = str(sys.argv[3])
B_player = str(sys.argv[4])

A_Wins_List = []
B_Wins_List = []
max_turns = 100


for _i_depth in range(MaxDepth):
    i_depth = _i_depth + 1
    A_Wins = 0
    B_Wins = 0
    for i_pos in range(len(Positions)):
        for i in range(2):
            board = LionBoard.LionBoard()
            board.setBoard_Fen(Positions[i_pos])
            whiteTurn = WhiteTurns[i_pos]
            turns = 0
            if i == 0:
                #print("Even Play")
                while not board.isGameOver():
                    if whiteTurn:
                        match A_player:
                            case "AlphaBeta":
                                evalAB, move = AlphaBeta.alpha_beta_simple(Depth, board, whiteTurn)
                                board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                            case "AlphaBeta-Quiescence":
                                evalAB, move = AlphaBeta.alpha_beta_simple(Depth, board, whiteTurn)
                                board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    else:
                        match B_player:
                            case "AlphaBeta":
                                evalAB, move = AlphaBeta.alpha_beta_simple(i_depth, board, whiteTurn)
                                board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                            case "AlphaBeta-Quiescence":
                                evalAB, move = AlphaBeta.alpha_beta_simple(i_depth, board, whiteTurn)
                                board.makeMove(whiteTurn, move.getFrom(), move.getTo())
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
                    if whiteTurn:
                        match B_player:
                            case "AlphaBeta":
                                evalAB, move = AlphaBeta.alpha_beta_simple(i_depth, board, whiteTurn)
                                board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                            case "AlphaBeta_Quiescence":
                                evalAB, move = AlphaBeta.alpha_beta_simple(i_depth, board, whiteTurn)
                                board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    else:
                        match A_player:
                            case "AlphaBeta":
                                evalAB, move = AlphaBeta.alpha_beta_simple(Depth, board, whiteTurn)
                                board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                            case "AlphaBeta_Quiescence":
                                evalAB, move = AlphaBeta.alpha_beta_simple(Depth, board, whiteTurn)
                                board.makeMove(whiteTurn, move.getFrom(), move.getTo())
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
        print(f"AB-{Depth} {A_Wins} : {B_Wins} AB-{i_depth}")
    A_Wins_List.append(A_Wins)
    B_Wins_List.append(B_Wins)

Path(f"./Resources/{A_player}-vs-{B_player}/Depth-{Depth}").mkdir(parents=True, exist_ok=True)
with open(f'./Resources/{A_player}-vs-{B_player}/Depth-{Depth}/{time.time()}.txt', 'a') as the_file:
    for i in range(len(A_Wins_List)):
        the_file.write(f"AB-{Depth} {A_Wins_List[i]}:{B_Wins_List[i]} AB-{i+1}\n")
