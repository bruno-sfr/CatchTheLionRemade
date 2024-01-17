from . import AB_Flag
#import AB_Flag

class HashEntry:
    def __init__(self, hash: int, depth: int, eval, fen: str, whiteturn: bool):
        self.Hash = hash
        self.Depth = depth
        self.Eval = eval
        self.Fen = fen
        self.whitetrun = whiteturn

    def getHash(self) -> int:
        return self.Hash
