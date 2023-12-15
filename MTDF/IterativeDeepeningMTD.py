import signal
from . import MTDF
#import MTDF
import time
from Game import LionBoard


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Function execution timed out.")


# Your function's code here
# Add some long-running computation or loop
class iterativeDeepeningMTD:
    def __init__(self):
        self.MTD = MTDF.MTDF()

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
                #eval, moves = self.MTD.MTDF(eval, depth, board, WhiteTurn, 0.1)
                # print("Depth:", depth)
                if depth % 2 == 0:
                    #print("Run Even")
                    evalMTD_even, moves = self.MTD.MTDF(evalMTD_even, depth, board, WhiteTurn, 0.1)
                else:
                    #print("Run Uneven")
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



if __name__ == "__main__":
    board = LionBoard.LionBoard()
    board.setBoard_start()
    ID = iterativeDeepeningMTD()

    eval, moves = ID.iterativeDeepening_MTD(5, board, True)
    print("eval:", eval)
    for i in moves:
        i.printMove()
