import signal
from . import AlphaBeta
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
        self.AB = AlphaBeta.Alpha_Beta_TranspostionTable()

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
                result = self.AB.alpha_beta_TT_simple(depth, board, WhiteTurn)
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
        depth = 1
        result = 0.0

        # Set the timeout handler for the SIGALRM signal
        signal.signal(signal.SIGALRM, timeout_handler)

        try:
            # Set the alarm to trigger after the specified timeout
            signal.alarm(timeout_seconds)

            # Call your function
            while True:
                result = AlphaBeta.alpha_beta_simple(depth, board, WhiteTurn)
                # print("Depth:", depth)
                depth = depth + 1

            # Disable the alarm since the function executed successfully
            # signal.alarm(0)
        except TimeoutError as e:
            print(e)
            # Handle the timeout event here (e.g., show an error message, take some action, etc.)
        return result


if __name__ == "__main__":
    board = LionBoard.LionBoard()
    board.setBoard_start()
    ID = iterativeDeepeningAB()

    eval, moves = ID.iterativeDeepening_AB_TT(5, board, True)
    print("eval:", eval)
    for i in moves:
        i.printMove()

    eval, moves = ID.iterativeDeepening_AB(5, board, True)
    print("eval:", eval)
    for i in moves:
        i.printMove()
