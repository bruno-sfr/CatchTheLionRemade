from Game import LionBoard, Move
from AlphaBeta import IterativeDeepening
from MonteCarlo import MCTS


def HumanVsHuman():
    board = LionBoard.LionBoard()
    board.setBoard_start()
    whiteTurn = True
    while True:
        board.printBoard()
        print("WhiteTurn:", whiteTurn)
        print("From?")
        __from = input()
        temp_from = str(__from)
        if temp_from == "c" or temp_from == "g" or temp_from == "e":
            _from = temp_from
        else:
            _from = int(__from)
        print("To?")
        _to = int(input())
        print(board.makeMove(whiteTurn, _from, _to))
        print("Has White won?", board.hasWhiteWon())
        whiteTurn = not whiteTurn


def ABvsMCTS():
    board = LionBoard.LionBoard()
    board.setBoard_start()
    AB = IterativeDeepening.iterativeDeepeningAB()
    whiteTurn = True
    while not board.isGameOver():
        board.printBoard()
        if whiteTurn:
            print("Alpha-Beta")
            eval, moves = AB.iterativeDeepening_AB_TT(10, board, whiteTurn)
            _from = moves[0].getFrom
            _tp = moves[0].getTo
            print("Move:", moves[0].printMove())
            print("Making Move:", board.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo()))
        else:
            print("MCTS")
            result = MCTS.MCTS(board, whiteTurn, 10)
            print("Move:", result.move.printMove())
            print("Making Move:", board.makeMove(whiteTurn, result.move.getFrom(), result.move.getTo()))
        whiteTurn = not whiteTurn
    board.printBoard()


if __name__ == '__main__':
    ABvsMCTS()
