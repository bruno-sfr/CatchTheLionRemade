class HashEntry:
    def __init__(self, hash: int, depth: int, eval, fen: str):
        self.Hash = hash
        self.Depth = depth
        self.Eval = eval
        self.Fen = fen

    def getHash(self) -> int:
        return self.Hash
