import numpy as np

class BitBoard:
    def __init__(self):
        self.bitboard = 0b0

    def setBoard(self, _bitboard):
        self.bitboard = _bitboard

    def getBoard(self):
        return self.bitboard

    def setSquare(self, square):
        if square > 11 or square < 0:
            return Exception("Argument outside of 11 to 0 inteval")
        self.bitboard |= (1 << square)

    def clearSquare(self, square):
        if square > 11 or square < 0:
            return Exception("Argument outside of 11 to 0 inteval")
        self.bitboard &= ~(1 << square)

    def isSquareSet(self, square):
        if square > 11 or square < 0:
            return Exception("Argument outside of 11 to 0 inteval")
        return (self.bitboard & (1 << square)) != 0

    def allSetSquares(self):
        list = []
        for i in range(12):
            if self.isSquareSet(i):
                list.append(i)
        return list

    def checksum(self):
        checksum = 0
        for i in range(12):
            if (self.bitboard & (1 << i)) != 0:
                checksum = checksum + 1
        return checksum

    def printBitBoard(self):
        for i in reversed(range(4)):
            for i2 in range(3):
                square = i*3+i2
                if self.isSquareSet(square):
                    print("1", end=" ")
                else:
                    print("0", end=" ")
            print()
