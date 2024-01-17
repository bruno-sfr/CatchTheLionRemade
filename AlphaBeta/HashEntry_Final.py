from . import AB_Flag
from Game import Move


# import AB_Flag

class HashEntry:
    def __init__(self, hash: int, depth: int, eval, flag: AB_Flag.Flag, Move: Move.Move):
        self.Hash = hash
        self.Depth = depth
        self.Eval = eval
        self.Flag = flag
        self.Move = Move

    def getHash(self) -> int:
        return self.Hash