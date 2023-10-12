class HashEntry:
    def __init__(self, hash: int, depth: int, lowerbound: float, upperbound: float):
        self.Hash = hash
        self.Depth = depth
        self.Lowerbound = lowerbound
        self.Upperbound = upperbound

    def getHash(self) -> int:
        return self.Hash
