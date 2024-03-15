import sys
from datetime import datetime
from pathlib import Path

from Game import LionBoard, Move
from AlphaBeta import IterativeDeepening, AlphaBeta
from MonteCarlo import MCTS_Solvers
import time

max_turns = 100
"""iterations = 0
game_time = 1
white_player = "MiniMax"
white_Depth = 1
white_Threshold = 1
black_player = "MiniMax"
black_Depth = 1
black_Threshold = 1
"""

if len(sys.argv) != 9:
    print("Missing Arguments, expected are in that order:")
    print("iterations game_time white_player white_Depth white_Threshold black_player black_Depth black_Threshold")
    exit()

iterations = int(sys.argv[1])
game_time = int(sys.argv[2])
white_player = str(sys.argv[3])
white_Depth = int(sys.argv[4])
white_Threshold = int(sys.argv[5])
black_player = str(sys.argv[6])
black_Depth = int(sys.argv[7])
black_Threshold = int(sys.argv[8])


white_wins = 0
white_sims = []
white_depths = []
black_wins = 0
black_sims = []
black_depths = []
#second = str(sys.argv[2])

for i in range(0, iterations):
    turns = 0
    board = LionBoard.LionBoard()
    board.setBoard_start()
    ID = IterativeDeepening.iterativeDeepeningAB()
    MTD = IterativeDeepening.iterativeDeepeningMTD()
    if i % 2 == 0:
        whiteTurn = True
    else:
        whiteTurn = False
    while not board.isGameOver():
        if whiteTurn:
            move = Move.Move()
            try:
                match white_player:
                    case "MiniMax":
                        eval, move, depth = ID.iterativeDeepening_MM(game_time, board, whiteTurn)
                        white_depths.append(depth)
                    case "Alpha_Beta":
                        eval, move, depth = ID.iterativeDeepening_AB(game_time, board, whiteTurn)
                        white_depths.append(depth)
                    case "Alpha_Beta_Fix":
                        eval, move = AlphaBeta.alpha_beta_simple(white_Depth, board, whiteTurn)
                    case "Alpha_Beta_TT":
                        eval, move, depth = ID.iterativeDeepening_AB_TT(game_time, board, whiteTurn)
                        white_depths.append(depth)
                    case "MTD":
                        eval, move, depth = MTD.iterativeDeepening_MTD(game_time, board, whiteTurn)
                        white_depths.append(depth)
                    case "MCTS_Solver":
                        ResultNode = MCTS_Solvers.MCTS_Solver_Run(board, whiteTurn, game_time)
                        white_sims.append(ResultNode.visits)
                        move = ResultNode.move
                    case "MCTS_MR":
                        ResultNode = MCTS_Solvers.MCTS_MR_Run(board, whiteTurn, game_time, white_Depth)
                        white_sims.append(ResultNode.visits)
                        move = ResultNode.move
                    case "MCTS_MS":
                        ResultNode = MCTS_Solvers.MCTS_MS_Run(board, whiteTurn, game_time, white_Threshold, white_Depth)
                        white_sims.append(ResultNode.visits)
                        move = ResultNode.move
                    case "MCTS_MB":
                        ResultNode = MCTS_Solvers.MCTS_MB_Run(board, whiteTurn, game_time, white_Depth)
                        white_sims.append(ResultNode.visits)
                        move = ResultNode.move
            except TimeoutError:
                print("Am i the problem?")
                pass
            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
        else:
            move = Move.Move()
            try:
                match black_player:
                    case "MiniMax":
                        eval, move, depth = ID.iterativeDeepening_MM(game_time, board, whiteTurn)
                        black_depths.append(depth)
                    case "Alpha_Beta":
                        eval, move, depth = ID.iterativeDeepening_AB(game_time, board, whiteTurn)
                        black_depths.append(depth)
                    case "Alpha_Beta_Fix":
                        eval, move = AlphaBeta.alpha_beta_simple(black_Depth, board, whiteTurn)
                    case "Alpha_Beta_TT":
                        eval, move, depth = ID.iterativeDeepening_AB_TT(game_time, board, whiteTurn)
                        black_depths.append(depth)
                    case "MTD":
                        eval, move, depth = MTD.iterativeDeepening_MTD(game_time, board, whiteTurn)
                        black_depths.append(depth)
                    case "MCTS_Solver":
                        ResultNode = MCTS_Solvers.MCTS_Solver_Run(board, whiteTurn, game_time)
                        black_sims.append(ResultNode.visits)
                        move = ResultNode.move
                    case "MCTS_MR":
                        ResultNode = MCTS_Solvers.MCTS_MR_Run(board, whiteTurn, game_time, black_Depth)
                        black_sims.append(ResultNode.visits)
                        move = ResultNode.move
                    case "MCTS_MS":
                        ResultNode = MCTS_Solvers.MCTS_MS_Run(board, whiteTurn, game_time, black_Threshold, black_Depth)
                        black_sims.append(ResultNode.visits)
                        move = ResultNode.move
                    case "MCTS_MB":
                        ResultNode = MCTS_Solvers.MCTS_MB_Run(board, whiteTurn, game_time, black_Depth)
                        black_sims.append(ResultNode.visits)
                        move = ResultNode.move
            except TimeoutError:
                #print("Am i the problem?")
                pass
            board.makeMove(whiteTurn, move.getFrom(), move.getTo())
        whiteTurn = not whiteTurn
        turns = turns + 1
        if turns > max_turns:
            break
    if board.hasWhiteWon():
        white_wins = white_wins + 1
    elif board.hasBlackWon():
        black_wins = black_wins + 1
    else:
        black_wins = black_wins + 0.5
        white_wins = white_wins + 0.5
    print(f"{white_player} {white_wins} : {black_wins} {black_player}")
print("Finished")

white_avg = 0
if len(white_sims) > 0:
    for sim in white_sims:
        white_avg = white_avg + sim
    white_avg = white_avg / len(white_sims)

white_avg_depth = 0
if len(white_depths) > 0:
    for depth in white_depths:
        white_avg_depth = white_avg_depth + depth
    white_avg_depth = white_avg_depth / len(white_depths)

black_avg = 0
if len(black_sims) > 0:
    for sim in black_sims:
        black_avg = black_avg + sim
    black_avg = black_avg / len(black_sims)

black_avg_depth = 0
if len(black_depths) > 0:
    for depth in black_depths:
        black_avg_depth = black_avg_depth + depth
    black_avg_depth = black_avg_depth / len(black_depths)

Path(f"/home/bruno.schaffer/CatchTheLionRemade/Resources/{white_player}-vs-{black_player}/{iterations}-{game_time}-{white_player}-{white_Depth}-{white_Threshold}-vs-{black_player}-{black_Depth}-{black_Threshold}").mkdir(parents=True, exist_ok=True)
with open(f'/home/bruno.schaffer/CatchTheLionRemade/Resources/{white_player}-vs-{black_player}/{iterations}-{game_time}-{white_player}-{white_Depth}-{white_Threshold}-vs-{black_player}-{black_Depth}-{black_Threshold}/{time.time()}.txt', 'a') as the_file:
    the_file.write(f"{white_wins}:{black_wins}\n")
    the_file.write(f"{white_avg}:{black_avg}\n")
    the_file.write(f"{white_avg_depth}:{black_avg_depth}\n")
    the_file.write(f"{white_player}:{black_player}\n")
    the_file.write(f"Average Simulation count: {white_avg}:{black_avg}\n")
    the_file.write(f"Average depth count: {white_avg_depth}:{black_avg_depth}\n")
    the_file.write(f"{white_player} Depth: {white_Depth} Threshold: {white_Threshold}\n")
    the_file.write(f"{black_player} Depth: {black_Depth} Threshold: {black_Threshold}\n")
"""Path(f"./Resources/{white_player}_vs_{black_player}/{iterations}_{game_time}_{white_player}_{white_Depth}_{white_Threshold}_vs_{black_player}_{black_Depth}_{black_Threshold}").mkdir(parents=True, exist_ok=True)
with open(f'./Resources/{white_player}_vs_{black_player}/{iterations}_{game_time}_{white_player}_{white_Depth}_{white_Threshold}_vs_{black_player}_{black_Depth}_{black_Threshold}/{time.time()}.txt', 'a') as the_file:
    the_file.write(f"{white_wins}:{black_wins}\n")
    the_file.write(f"{white_player}:{black_player}\n")
    the_file.write(f"Average Simulation count: {white_avg}:{black_avg}\n")
    the_file.write(f"{white_player} Depth: {white_Depth} Threshold: {white_Threshold}\n")
    the_file.write(f"{black_player} Depth: {black_Depth} Threshold: {black_Threshold}\n")"""
