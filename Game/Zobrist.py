import random
from Game import LionBoard
from Game import BitBoard


class Zobrist:
    def __init__(self):
        self.whiteTurnRand = random.getrandbits(32)
        self.blackTurnRand = random.getrandbits(32)
        self.whitelionRandoms = []
        self.whitechickenRandoms = []
        self.whitehenRandoms = []
        self.whiteelephantRandoms = []
        self.whitegiraffeRandoms = []
        self.blacklionRandoms = []
        self.blackchickenRandoms = []
        self.blackhenRandoms = []
        self.blackelephantRandoms = []
        self.blackgiraffeRandoms = []
        self.whiteReserveRandoms = []
        self.blackReserveRandoms = []

        for i in range(0, 12):
            rand = random.getrandbits(32)
            self.whitelionRandoms.append(rand)
            rand = random.getrandbits(32)
            self.whitechickenRandoms.append(rand)
            rand = random.getrandbits(32)
            self.whitehenRandoms.append(rand)
            rand = random.getrandbits(32)
            self.whiteelephantRandoms.append(rand)
            rand = random.getrandbits(32)
            self.whitegiraffeRandoms.append(rand)
            rand = random.getrandbits(32)
            self.blacklionRandoms.append(rand)
            rand = random.getrandbits(32)
            self.blackchickenRandoms.append(rand)
            rand = random.getrandbits(32)
            self.blackhenRandoms.append(rand)
            rand = random.getrandbits(32)
            self.blackelephantRandoms.append(rand)
            rand = random.getrandbits(32)
            self.blackgiraffeRandoms.append(rand)

        for i in range(0, 6):
            rand = random.getrandbits(32)
            self.whiteReserveRandoms.append(rand)
            rand = random.getrandbits(32)
            self.blackReserveRandoms.append(rand)

    def generateHash(self, board: LionBoard.LionBoard, whiteTurn: bool):
        hash = 0

        if whiteTurn:
            hash = hash ^ self.whiteTurnRand
        else:
            hash = hash ^ self.blackTurnRand

        whitelionBoard = BitBoard.BitBoard()
        whitelionBoard.setBoard(board.white.getBoard() & board.lion.getBoard())
        whitelions = whitelionBoard.allSetSquares()
        for i in whitelions:
            hash = hash ^ self.whitelionRandoms[i]

        whitechickenBoard = BitBoard.BitBoard()
        whitechickenBoard.setBoard(board.white.getBoard() & board.chicken.getBoard())
        whitechickens = whitechickenBoard.allSetSquares()
        for i in whitechickens:
            hash = hash ^ self.whitechickenRandoms[i]

        whitehenBoard = BitBoard.BitBoard()
        whitehenBoard.setBoard(board.white.getBoard() & board.hen.getBoard())
        whitehens = whitehenBoard.allSetSquares()
        for i in whitehens:
            hash = hash ^ self.whitehenRandoms[i]

        whiteelephantBoard = BitBoard.BitBoard()
        whiteelephantBoard.setBoard(board.white.getBoard() & board.elephant.getBoard())
        whiteelephants = whiteelephantBoard.allSetSquares()
        for i in whiteelephants:
            hash = hash ^ self.whiteelephantRandoms[i]

        whitegiraffeBoard = BitBoard.BitBoard()
        whitegiraffeBoard.setBoard(board.white.getBoard() & board.giraffe.getBoard())
        whitegiraffes = whitegiraffeBoard.allSetSquares()
        for i in whitegiraffes:
            hash = hash ^ self.whitegiraffeRandoms[i]


        blacklionBoard = BitBoard.BitBoard()
        blacklionBoard.setBoard(board.black.getBoard() & board.lion.getBoard())
        blacklions = blacklionBoard.allSetSquares()
        for i in blacklions:
            hash = hash ^ self.blacklionRandoms[i]

        blackchickenBoard = BitBoard.BitBoard()
        blackchickenBoard.setBoard(board.black.getBoard() & board.chicken.getBoard())
        blackchickens = blackchickenBoard.allSetSquares()
        for i in blackchickens:
            hash = hash ^ self.blackchickenRandoms[i]

        blackhenBoard = BitBoard.BitBoard()
        blackhenBoard.setBoard(board.black.getBoard() & board.hen.getBoard())
        blackhens = blackhenBoard.allSetSquares()
        for i in blackhens:
            hash = hash ^ self.blackhenRandoms[i]

        blackelephantBoard = BitBoard.BitBoard()
        blackelephantBoard.setBoard(board.black.getBoard() & board.elephant.getBoard())
        blackelephants = blackelephantBoard.allSetSquares()
        for i in blackelephants:
            hash = hash ^ self.blackelephantRandoms[i]

        blackgiraffeBoard = BitBoard.BitBoard()
        blackgiraffeBoard.setBoard(board.black.getBoard() & board.giraffe.getBoard())
        blackgiraffes = blackgiraffeBoard.allSetSquares()
        for i in blackgiraffes:
            hash = hash ^ self.blackgiraffeRandoms[i]

        if board.white_captures.__contains__("chicken"):
            hash = hash ^ self.whiteReserveRandoms[0]
        else:
            hash = hash ^ self.whiteReserveRandoms[1]

        if board.white_captures.__contains__("elephant"):
            hash = hash ^ self.whiteReserveRandoms[2]
        else:
            hash = hash ^ self.whiteReserveRandoms[3]

        if board.white_captures.__contains__("giraffe"):
            hash = hash ^ self.whiteReserveRandoms[4]
        else:
            hash = hash ^ self.whiteReserveRandoms[5]

        if board.black_captures.__contains__("chicken"):
            hash = hash ^ self.blackReserveRandoms[0]
        else:
            hash = hash ^ self.blackReserveRandoms[1]

        if board.black_captures.__contains__("elephant"):
            hash = hash ^ self.blackReserveRandoms[2]
        else:
            hash = hash ^ self.blackReserveRandoms[3]

        if board.black_captures.__contains__("giraffe"):
            hash = hash ^ self.blackReserveRandoms[4]
        else:
            hash = hash ^ self.blackReserveRandoms[5]

        return hash


if __name__ == '__main__':
    zob = Zobrist()
    board = LionBoard.LionBoard()
    board.setBoard_Fen("3/1l1/2L/C2/GgcEe")
    board2 = LionBoard.LionBoard()
    board2.setBoard_Fen("3/1L1/2l/C2/GgcEe")
    print(zob.generateHash(board, True))
    print(zob.generateHash(board2, True))
    """board.setBoard_start()
    print(zob.generateHash(board, True))
    board.makeRandomMove(True)
    print(zob.generateHash(board, True))"""
