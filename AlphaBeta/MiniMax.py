import copy
from Game import LionBoard

def MiniMax(depth: int, board: LionBoard.LionBoard, whiteTurn: bool, moves: list):
    if depth == 0:
        eval = board.eval_func()
        return eval, moves

    if board.isGameOver():
        eval = board.eval_func()
        return eval, moves

    best_moves = copy.deepcopy(moves)

    if whiteTurn:
        maxEval = float('-inf')
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
                new_whiteTurn = not whiteTurn
                eval, move_list = MiniMax(depth - 1, new_board, new_whiteTurn, new_moves)
                if eval > maxEval:
                    maxEval = eval
                    best_moves = move_list
                # elif eval == maxEval:
                # add a random element to selection of equal value
                #    rand = random.randint(0, 1)
                #    if rand == 1:
                #        maxEval = eval
                # bestmove = move
                #        best_moves = move_list
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
                new_whiteTurn = not whiteTurn
                eval, move_list = MiniMax(depth - 1, new_board, new_whiteTurn, new_moves)
                if eval < minEval:
                    minEval = eval
                    best_moves = move_list
                # elif eval == minEval:
                # add a random element to selection of equal value
                #    rand = random.randint(0, 1)
                #    if rand == 1:
                #        minEval = eval
                # bestmove = move
                #        best_moves = move_list
        return minEval, best_moves