import signal
from . import AlphaBeta, MiniMax
#import AlphaBeta
import time
from Game import LionBoard


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out.")


# Your function's code here
# Add some long-running computation or loop
class iterativeDeepeningAB:
    def __init__(self):
        self.AB = AlphaBeta.Alpha_Beta_TT_Final()
        self.depth = 1

    def iterativeDeepening_AB_TT(self, time: int, board: LionBoard.LionBoard, WhiteTurn: bool):
        # Set the timeout in seconds
        timeout_seconds = time
        depth = 1
        result = 0.0

        # Set the timeout handler for the SIGALRM signal
        signal.signal(signal.SIGALRM, timeout_handler)

        try:
            # Set the alarm to trigger after the specified timeout
            signal.alarm(timeout_seconds)

            # Call your function
            while True:
                result = self.AB.alpha_beta_TT_final_simple(depth, board, WhiteTurn)
                # print("Depth:", depth)
                depth = depth + 1

            # Disable the alarm since the function executed successfully
            # signal.alarm(0)
        except TimeoutError as e:
            print(e)
            # Handle the timeout event here (e.g., show an error message, take some action, etc.)
        return result

    def iterativeDeepening_AB(self, time: int, board: LionBoard.LionBoard, WhiteTurn: bool):
        # Set the timeout in seconds
        timeout_seconds = time
        self.depth = 1
        result = 0.0

        # Set the timeout handler for the SIGALRM signal
        signal.signal(signal.SIGALRM, timeout_handler)

        try:
            # Set the alarm to trigger after the specified timeout
            signal.alarm(timeout_seconds)

            # Call your function
            while True:
                result = AlphaBeta.alpha_beta_simple(self.depth, board, WhiteTurn)
                # print("Depth:", depth)
                self.depth = self.depth + 1

            # Disable the alarm since the function executed successfully
            # signal.alarm(0)
        except TimeoutError as e:
            print(f"Depth {self.depth} reached")
            # Handle the timeout event here (e.g., show an error message, take some action, etc.)
        return result

    def iterativeDeepening_MM(self, time: int, board: LionBoard.LionBoard, WhiteTurn: bool):
        # Set the timeout in seconds
        timeout_seconds = time
        self.depth = 1
        result = 0.0

        # Set the timeout handler for the SIGALRM signal
        signal.signal(signal.SIGALRM, timeout_handler)

        try:
            # Set the alarm to trigger after the specified timeout
            signal.alarm(timeout_seconds)

            # Call your function
            while True:
                result = MiniMax.MiniMax(self.depth, board, WhiteTurn, [])
                # print("Depth:", depth)
                self.depth = self.depth + 1

            # Disable the alarm since the function executed successfully
            # signal.alarm(0)
        except TimeoutError as e:
            # print(e)
            print(f"Depht {self.depth} reached")
            # Handle the timeout event here (e.g., show an error message, take some action, etc.)
        return result


if __name__ == "__main__":
    board = LionBoard.LionBoard()
    board.setBoard_start()
    board.setBoard_Fen("elc/1C1/G11/1LE/G")
    board.printBoard()
    ID = iterativeDeepeningAB()

    """board.makeMove(True,7,10)
    board.printBoard()
    print("Eval:", board.eval_func())"""

    """eval, moves = ID.iterativeDeepening_AB_TT(5, board, True)
    print("eval:", eval)
    for i in moves:
        i.printMove()"""

    eval, moves = AlphaBeta.alpha_beta_simple(3,board,False)

    print("eval:", eval)
    for i in moves:
        i.printMove()

    """eval, moves = ID.iterativeDeepening_AB(1, board, False)
    print("eval:", eval)
    for i in moves:
        i.printMove()
    print("Depth:", ID.depth)"""
