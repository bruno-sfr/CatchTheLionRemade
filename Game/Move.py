class Move:
    def __init__(self):
        self._from = 0
        self._to = 0

    def setMove(self, __from, __to):
        self._from = __from
        self._to = __to

    def getFrom(self):
        return self._from

    def getTo(self):
        return  self._to

    def setFrom(self, __from):
        self._from = __from

    def setTo(self, __to):
        self._to = __to

    def equals(self, move):
        if self._to == move._to and self._from == move._from:
            return True
        else:
            return False

    def printMove(self):
        print("From:", self._from, " To:", self._to)


"""
move1 = Move()
move1.setMove(1, 2)
move2 = Move()
move2.setMove(2, 2)
print(move1.equals(move2))
"""