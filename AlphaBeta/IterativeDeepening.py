import signal
from . import AlphaBeta
#import AlphaBeta
import time
from Game import LionBoard


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out.")

class iterativeDeepeningMTD:
    def __init__(self):
        self.MTD = AlphaBeta.MTDF()

    def iterativeDeepening_MTD(self, time: int, board: LionBoard.LionBoard, WhiteTurn: bool):
        # Set the timeout in seconds
        timeout_seconds = time
        depth = 1
        #eval = 0.0
        evalMTD_even = 0.0
        evalMTD_uneven = 0.0
        moves = []

        # Set the timeout handler for the SIGALRM signal
        signal.signal(signal.SIGALRM, timeout_handler)

        try:
            # Set the alarm to trigger after the specified timeout
            signal.alarm(timeout_seconds)

            # Call your function
            while True:
                if depth % 2 == 0:
                    evalMTD_even, moves = self.MTD.MTDF(evalMTD_even, depth, board, WhiteTurn, 0.1)
                else:
                    evalMTD_uneven, moves = self.MTD.MTDF(evalMTD_uneven, depth, board, WhiteTurn, 0.1)
                depth = depth + 1
            # Disable the alarm since the function executed successfully
            # signal.alarm(0)
        except TimeoutError as e:
            print(e)
            # Handle the timeout event here (e.g., show an error message, take some action, etc.)
        if depth % 2 == 0:
            return evalMTD_even, moves
        else:
            return evalMTD_uneven, moves
        #return eval, moves

class iterativeDeepeningAB:
    def __init__(self):
        self.AB = AlphaBeta.Alpha_Beta_TT()
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
                result = AlphaBeta.MiniMax(self.depth, board, WhiteTurn)
                # print("Depth:", depth)
                self.depth = self.depth + 1

            # Disable the alarm since the function executed successfully
            # signal.alarm(0)
        except TimeoutError as e:
            pass
            # print(e)
            #print(f"Depht {self.depth} reached")
            # Handle the timeout event here (e.g., show an error message, take some action, etc.)
        return result