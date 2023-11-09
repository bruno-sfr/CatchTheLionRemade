import random
from Game import BitBoard
from Game import Move

class LionBoard:
    def __init__(self):
        self.white = BitBoard.BitBoard()
        self.black = BitBoard.BitBoard()
        self.lion = BitBoard.BitBoard()
        self.elephant = BitBoard.BitBoard()
        self.giraffe = BitBoard.BitBoard()
        self.chicken = BitBoard.BitBoard()
        self.hen = BitBoard.BitBoard()
        # in written String lower case
        self.black_captures = []
        self.white_captures = []
        # self.captures = BitBoard.BitBoard()
        self.lion_moves = [0b000000011010, 0b000000111101, 0b000000110010, 0b000011010011,
                           0b000111101111, 0b000110010110, 0b011010011000, 0b111101111000,
                           0b110010110000, 0b010011000000, 0b101111000000, 0b010110000000]
        self.giraffe_moves = [0b000000001010, 0b000000010101, 0b000000100010, 0b000001010001,
                              0b000010101010, 0b000100010100, 0b001010001000, 0b010101010000,
                              0b100010100000, 0b010001000000, 0b101010000000, 0b010100000000]
        self.elephant_moves = [0b000000010000, 0b000000101000, 0b000000010000, 0b000010000010,
                               0b000101000101, 0b000010000010, 0b010000010000, 0b101000101000,
                               0b010000010000, 0b000010000000, 0b000101000000, 0b000010000000]
        self.chicken_white_moves = [0b000000001000, 0b000000010000, 0b000000100000, 0b000001000000,
                                    0b000010000000, 0b000100000000, 0b001000000000, 0b010000000000,
                                    0b100000000000, 0b000000000000, 0b000000000000, 0b000000000000]
        self.chicken_black_moves = [0b000000000000, 0b000000000000, 0b000000000000, 0b000000000001,
                                    0b000000000010, 0b000000000100, 0b000000001000, 0b000000010000,
                                    0b000000100000, 0b000001000000, 0b000010000000, 0b000100000000]
        self.hen_white_moves = [0b000000011010, 0b000000111101, 0b000000110010, 0b000011010001,
                                0b000111101010, 0b000110010100, 0b011010001000, 0b111101010000,
                                0b110010100000, 0b010001000000, 0b101010000000, 0b010100000000]
        self.hen_black_moves = [0b000000001010, 0b000000010101, 0b000000100010, 0b000001010011,
                                0b000010101111, 0b000100010110, 0b001010011000, 0b010101111000,
                                0b100010110000, 0b010011000000, 0b101111000000, 0b010110000000]
        """
        for i in self.hen_white_moves:
            temp = BitBoard.BitBoard()
            temp.setBoard(i)
            temp.printBitBoard()
            print()
        """

    def setBoard_start(self):
        self.white.setBoard(0b000000010111)
        self.black.setBoard(0b111010000000)
        self.lion.setBoard(0b010000000010)
        self.elephant.setBoard(0b100000000001)
        self.giraffe.setBoard(0b001000000100)
        self.chicken.setBoard(0b000010010000)
        self.hen.setBoard(0b000000000000)
        # self.captures.setBoard(0b000000000000)

    def setBoard_Fen(self, Fen: str):
        self.white.setBoard(0b000000000000)
        self.black.setBoard(0b000000000000)
        self.lion.setBoard(0b000000000000)
        self.elephant.setBoard(0b000000000000)
        self.giraffe.setBoard(0b000000000000)
        self.chicken.setBoard(0b000000000000)
        self.hen.setBoard(0b000000000000)
        self.black_captures = []
        self.white_captures = []
        i = 11
        for char in Fen:
            if char.isdigit():
                i = i - int(char)
            elif i < 0:
                # captures
                if char == 'E':
                    self.white_captures.append("elephant")
                elif char == 'G':
                    self.white_captures.append("giraffe")
                elif char == 'C':
                    self.white_captures.append("chicken")
                elif char == 'e':
                    self.black_captures.append("elephant")
                elif char == 'g':
                    self.black_captures.append("giraffe")
                elif char == 'c':
                    self.black_captures.append("chicken")
            elif char == 'L':
                self.white.setSquare(i)
                self.lion.setSquare(i)
                i = i - 1
            elif char == 'E':
                self.white.setSquare(i)
                self.elephant.setSquare(i)
                i = i - 1
            elif char == 'G':
                self.white.setSquare(i)
                self.giraffe.setSquare(i)
                i = i - 1
            elif char == 'C':
                self.white.setSquare(i)
                self.chicken.setSquare(i)
                i = i - 1
            elif char == 'H':
                self.white.setSquare(i)
                self.hen.setSquare(i)
                i = i - 1
            elif char == 'l':
                self.black.setSquare(i)
                self.lion.setSquare(i)
                i = i - 1
            elif char == 'e':
                self.black.setSquare(i)
                self.elephant.setSquare(i)
                i = i - 1
            elif char == 'g':
                self.black.setSquare(i)
                self.giraffe.setSquare(i)
                i = i - 1
            elif char == 'c':
                self.black.setSquare(i)
                self.chicken.setSquare(i)
                i = i - 1
            elif char == 'h':
                self.black.setSquare(i)
                self.hen.setSquare(i)
                i = i - 1

    def setBoard(self, board):
        self.white.setBoard(board.white.getBoard())
        self.black.setBoard(board.black.getBoard())
        self.lion.setBoard(board.lion.getBoard())
        self.elephant.setBoard(board.elephant.getBoard())
        self.giraffe.setBoard(board.giraffe.getBoard())
        self.chicken.setBoard(board.chicken.getBoard())
        self.hen.setBoard(board.hen.getBoard())

    def getFen(self):
        Fen = ""
        for i in reversed(range(0,12)):
            if self.white.isSquareSet(i):
                if self.lion.isSquareSet(i):
                    Fen = Fen + "L"
                elif self.elephant.isSquareSet(i):
                    Fen = Fen + "E"
                elif self.giraffe.isSquareSet(i):
                    Fen = Fen + "G"
                elif self.chicken.isSquareSet(i):
                    Fen = Fen + "C"
                elif self.hen.isSquareSet(i):
                    Fen = Fen + "H"
            elif self.black.isSquareSet(i):
                if self.lion.isSquareSet(i):
                    Fen = Fen + "l"
                elif self.elephant.isSquareSet(i):
                    Fen = Fen + "e"
                elif self.giraffe.isSquareSet(i):
                    Fen = Fen + "g"
                elif self.chicken.isSquareSet(i):
                    Fen = Fen + "c"
                elif self.hen.isSquareSet(i):
                    Fen = Fen + "h"
            else:
                Fen = Fen + "1"
            if i%3 == 0:
                Fen = Fen + "/"

        for animal in self.black_captures:
            if animal == "giraffe":
                Fen = Fen + "g"
            elif animal == "chicken":
                Fen = Fen + "c"
            elif animal == "elephant":
                Fen = Fen + "e"

        for animal in self.white_captures:
            if animal == "giraffe":
                Fen = Fen + "G"
            elif animal == "chicken":
                Fen = Fen + "C"
            elif animal == "elephant":
                Fen = Fen + "E"
        return Fen

    def randomBoard(self):
        self.white.setBoard(0b000000000000)
        self.black.setBoard(0b000000000000)
        self.lion.setBoard(0b000000000000)
        self.elephant.setBoard(0b000000000000)
        self.giraffe.setBoard(0b000000000000)
        self.chicken.setBoard(0b000000000000)
        self.hen.setBoard(0b000000000000)
        self.black_captures = []
        self.white_captures = []

        # lions
        # white
        rand = random.randint(0, 11)
        if not (self.white.isSquareSet(rand)) and not (self.black.isSquareSet(rand)):
            self.white.setSquare(rand)
            self.lion.setSquare(rand)

        # black
        rand = random.randint(0, 11)
        if not (self.white.isSquareSet(rand)) and not (self.black.isSquareSet(rand)):
            self.black.setSquare(rand)
            self.lion.setSquare(rand)

        # giraffe
        # black
        rand = random.randint(0, 11)
        if not (self.white.isSquareSet(rand)) and not (self.black.isSquareSet(rand)):
            self.black.setSquare(rand)
            self.giraffe.setSquare(rand)
        else:
            self.white_captures.append("giraffe")

        # white
        rand = random.randint(0, 11)
        if not (self.white.isSquareSet(rand)) and not (self.black.isSquareSet(rand)):
            self.white.setSquare(rand)
            self.giraffe.setSquare(rand)
        else:
            self.black_captures.append("giraffe")

        # elephant
        # white
        rand = random.randint(0, 11)
        if not (self.white.isSquareSet(rand)) and not (self.black.isSquareSet(rand)):
            self.white.setSquare(rand)
            self.elephant.setSquare(rand)
        else:
            self.black_captures.append("elephant")

        rand = random.randint(0, 11)
        if not (self.white.isSquareSet(rand)) and not (self.black.isSquareSet(rand)):
            self.black.setSquare(rand)
            self.elephant.setSquare(rand)
        else:
            self.white_captures.append("elephant")

        # chicken and hen
        # black
        rand = random.randint(0, 1)
        if rand == 1:
            rand = random.randint(3, 11)
            if not (self.white.isSquareSet(rand)) and not (self.black.isSquareSet(rand)):
                self.black.setSquare(rand)
                self.chicken.setSquare(rand)
            else:
                self.white_captures.append("chicken")
        else:
            rand = random.randint(0, 11)
            if not (self.white.isSquareSet(rand)) and not (self.black.isSquareSet(rand)):
                self.black.setSquare(rand)
                self.hen.setSquare(rand)
            else:
                self.white_captures.append("chicken")

        # white
        rand = random.randint(0, 1)
        if rand == 1:
            rand = random.randint(0, 8)
            if not (self.white.isSquareSet(rand)) and not (self.black.isSquareSet(rand)):
                self.white.setSquare(rand)
                self.chicken.setSquare(rand)
            else:
                self.black_captures.append("chicken")
        else:
            rand = random.randint(0, 11)
            if not (self.white.isSquareSet(rand)) and not (self.black.isSquareSet(rand)):
                self.white.setSquare(rand)
                self.hen.setSquare(rand)
            else:
                self.black_captures.append("chicken")

    def allpossibleMoves_BigList(self, whiteTurn:bool):
        list = self.allpossibleMoves(whiteTurn)
        big_list = []
        for sub_list in list:
            for move in sub_list:
                big_list.append(move)
        return big_list

    def allpossibleMoves(self, whiteTurn: bool):
        # lion, giraffe, elephant, chicken, hen, capture
        list = []
        lion_list = []
        giraffe_list = []
        elephant_list = []
        chicken_list = []
        hen_list = []
        capture_list = []

        if whiteTurn:
            white_lion = BitBoard.BitBoard()
            white_lion.setBoard(self.lion.getBoard() & self.white.getBoard())
            lion = white_lion.allSetSquares()
            white_giraffe = BitBoard.BitBoard()
            white_giraffe.setBoard(self.giraffe.getBoard() & self.white.getBoard())
            giraffe = white_giraffe.allSetSquares()
            white_elephant = BitBoard.BitBoard()
            white_elephant.setBoard(self.elephant.getBoard() & self.white.getBoard())
            elephant = white_elephant.allSetSquares()
            white_chicken = BitBoard.BitBoard()
            white_chicken.setBoard(self.chicken.getBoard() & self.white.getBoard())
            chicken = white_chicken.allSetSquares()
            white_hen = BitBoard.BitBoard()
            white_hen.setBoard(self.hen.getBoard() & self.white.getBoard())
            hen = white_hen.allSetSquares()
            Attacker = self.white.getBoard()
            Defender = self.black.getBoard()
            Captures = self.white_captures
        else:
            black_lion = BitBoard.BitBoard()
            black_lion.setBoard(self.lion.getBoard() & self.black.getBoard())
            lion = black_lion.allSetSquares()
            black_giraffe = BitBoard.BitBoard()
            black_giraffe.setBoard(self.giraffe.getBoard() & self.black.getBoard())
            giraffe = black_giraffe.allSetSquares()
            black_elephant = BitBoard.BitBoard()
            black_elephant.setBoard(self.elephant.getBoard() & self.black.getBoard())
            elephant = black_elephant.allSetSquares()
            black_chicken = BitBoard.BitBoard()
            black_chicken.setBoard(self.chicken.getBoard() & self.black.getBoard())
            chicken = black_chicken.allSetSquares()
            black_hen = BitBoard.BitBoard()
            black_hen.setBoard(self.hen.getBoard() & self.black.getBoard())
            hen = black_hen.allSetSquares()
            Attacker = self.black.getBoard()
            Defender = self.white.getBoard()
            Captures = self.black_captures

        # lion
        for i in lion:
            temp = BitBoard.BitBoard()
            temp.setBoard(self.lion_moves[i] & ~Attacker)
            temp_list = temp.allSetSquares()
            for i2 in temp_list:
                move = Move.Move()
                move.setMove(i, i2)
                lion_list.append(move)
        list.append(lion_list)

        # giraffe
        for i in giraffe:
            temp = BitBoard.BitBoard()
            temp.setBoard(self.giraffe_moves[i] & ~Attacker)
            temp_list = temp.allSetSquares()
            for i2 in temp_list:
                move = Move.Move()
                move.setMove(i, i2)
                giraffe_list.append(move)
        list.append(giraffe_list)

        # elephant
        for i in elephant:
            temp = BitBoard.BitBoard()
            temp.setBoard(self.elephant_moves[i] & ~Attacker)
            temp_list = temp.allSetSquares()
            for i2 in temp_list:
                move = Move.Move()
                move.setMove(i, i2)
                elephant_list.append(move)
        list.append(elephant_list)

        # chicken
        if whiteTurn:
            for i in chicken:
                temp = BitBoard.BitBoard()
                temp.setBoard(self.chicken_white_moves[i] & ~Attacker)
                temp_list = temp.allSetSquares()
                for i2 in temp_list:
                    move = Move.Move()
                    move.setMove(i, i2)
                    chicken_list.append(move)
        else:
            for i in chicken:
                temp = BitBoard.BitBoard()
                temp.setBoard(self.chicken_black_moves[i] & ~Attacker)
                temp_list = temp.allSetSquares()
                for i2 in temp_list:
                    move = Move.Move()
                    move.setMove(i, i2)
                    chicken_list.append(move)
        list.append(chicken_list)

        # hen
        if whiteTurn:
            for i in hen:
                temp = BitBoard.BitBoard()
                temp.setBoard(self.hen_white_moves[i] & ~Attacker)
                temp_list = temp.allSetSquares()
                for i2 in temp_list:
                    move = Move.Move()
                    move.setMove(i, i2)
                    hen_list.append(move)
        else:
            for i in hen:
                temp = BitBoard.BitBoard()
                temp.setBoard(self.hen_black_moves[i] & ~Attacker)
                temp_list = temp.allSetSquares()
                for i2 in temp_list:
                    move = Move.Move()
                    move.setMove(i, i2)
                    hen_list.append(move)
        list.append(hen_list)

        __freefields = ~(self.black.getBoard() | self.white.getBoard())
        _freefields = BitBoard.BitBoard()
        _freefields.setBoard(__freefields)
        freefields = _freefields.allSetSquares()

        for piece in Captures:
            if piece == "giraffe":
                for field in freefields:
                    move = Move.Move()
                    move.setMove("g", field)
                    """"if whiteTurn:
                        move.setMove("G", field)
                    else:
                        move.setMove("g", field)"""
                    capture_list.append(move)
            elif piece == "elephant":
                for field in freefields:
                    move = Move.Move()
                    move.setMove("e", field)
                    """if whiteTurn:
                        move.setMove("E", field)
                    else:
                        move.setMove("G", field)"""
                    capture_list.append(move)
            elif piece == "chicken":
                if whiteTurn:
                    _chicken_freefields = BitBoard.BitBoard()
                    lastrow = 0b111000000000
                    _chicken_freefields.setBoard(__freefields & ~lastrow)
                    chicken_freefields = _chicken_freefields.allSetSquares()
                else:
                    _chicken_freefields = BitBoard.BitBoard()
                    lastrow = 0b000000000111
                    _chicken_freefields.setBoard(__freefields & ~lastrow)
                    chicken_freefields = _chicken_freefields.allSetSquares()
                for field in chicken_freefields:
                    move = Move.Move()
                    move.setMove("c", field)
                    """if whiteTurn:
                        move.setMove("C", field)
                    else:
                        move.setMove("c", field)"""
                    capture_list.append(move)
        list.append(capture_list)

        return list

    def makeRandomMove(self,  whiteTurn: bool):
        MAX_ITERATIONS = 10
        i = 0
        list = self.allpossibleMoves(whiteTurn)
        rand = random.randint(0, 5)
        while len(list[rand]) == 0:
            if len(list[rand]) == 0 and i < MAX_ITERATIONS:
                rand = random.randint(0, 5)
                i = i + 1
            if i == MAX_ITERATIONS:
                return

        if len(list[rand]) > 1:
            rand2 = random.randint(0, len(list[rand]) - 1)
        else:
            rand2 = 0
        move = Move.Move()
        move.setMove(list[rand][rand2].getFrom(), list[rand][rand2].getTo())
        self.makeMove(whiteTurn, move.getFrom(), move.getTo())
        return move

    def check_hen(self, whiteTurn: bool):
        chick = BitBoard.BitBoard()
        if whiteTurn:
            chick.setBoard(self.chicken.getBoard() & self.white.getBoard())
            for i in range(9, 12):
                if chick.isSquareSet(i):
                    self.chicken.clearSquare(i)
                    self.hen.setSquare(i)
        else:
            chick.setBoard(self.chicken.getBoard() & self.black.getBoard())
            for i in range(3):
                if chick.isSquareSet(i):
                    self.chicken.clearSquare(i)
                    self.hen.setSquare(i)

    def makeMove(self, whiteTurn: bool, _from, _to):
        move = Move.Move()
        move.setMove(_from, _to)
        if whiteTurn:
            allMoves = self.allpossibleMoves(True)
            Attacker = self.white
            Defender = self.black
            Captures = self.white_captures
        else:
            allMoves = self.allpossibleMoves(False)
            Attacker = self.black
            Defender = self.white
            Captures = self.black_captures
        lion_moves = allMoves[0]
        giraffe_moves = allMoves[1]
        elephant_moves = allMoves[2]
        chicken_moves = allMoves[3]
        hen_moves = allMoves[4]
        capture_moves = allMoves[5]

        for imove in lion_moves:
            if imove.equals(move):
                self.pieceMove(Attacker, Defender, move, Captures, self.lion)
                return True
        for imove in giraffe_moves:
            if imove.equals(move):
                self.pieceMove(Attacker, Defender, move, Captures, self.giraffe)
                return True
        for imove in elephant_moves:
            if imove.equals(move):
                self.pieceMove(Attacker, Defender, move, Captures, self.elephant)
                return True
        for imove in chicken_moves:
            if imove.equals(move):
                self.pieceMove(Attacker, Defender, move, Captures, self.chicken)
                self.check_hen(whiteTurn)
                return True
        for imove in hen_moves:
            if imove.equals(move):
                self.pieceMove(Attacker, Defender, move, Captures, self.hen)
                return True

        for imove in capture_moves:
            if imove.equals(move):
                if move.getFrom() == "g":
                    Captures.remove("giraffe")
                    Attacker.setSquare(move.getTo())
                    self.giraffe.setSquare(move.getTo())
                elif move.getFrom() == "e":
                    Captures.remove("elephant")
                    Attacker.setSquare(move.getTo())
                    self.elephant.setSquare(move.getTo())
                elif move.getFrom() == "c":
                    Captures.remove("chicken")
                    Attacker.setSquare(move.getTo())
                    self.chicken.setSquare(move.getTo())
                return True

        return False

    def pieceMove(self, attacker: BitBoard, defender: BitBoard, move: Move, captures: [], piece_type: BitBoard):
        defender_lion = BitBoard.BitBoard()
        defender_lion.setBoard(self.lion.getBoard() & defender.getBoard())
        defender_giraffe = BitBoard.BitBoard()
        defender_giraffe.setBoard(self.giraffe.getBoard() & defender.getBoard())
        defender_elephant = BitBoard.BitBoard()
        defender_elephant.setBoard(self.elephant.getBoard() & defender.getBoard())
        defender_chicken = BitBoard.BitBoard()
        defender_chicken.setBoard(self.chicken.getBoard() & defender.getBoard())
        defender_hen = BitBoard.BitBoard()
        defender_hen.setBoard(self.hen.getBoard() & defender.getBoard())

        if defender.isSquareSet(move.getTo()):
            defender.clearSquare(move.getTo())
            if defender_lion.isSquareSet(move.getTo()):
                self.lion.clearSquare(move.getTo())
            elif defender_giraffe.isSquareSet(move.getTo()):
                self.giraffe.clearSquare(move.getTo())
                captures.append("giraffe")
            elif defender_elephant.isSquareSet(move.getTo()):
                self.elephant.clearSquare(move.getTo())
                captures.append("elephant")
            elif defender_chicken.isSquareSet(move.getTo()):
                self.chicken.clearSquare(move.getTo())
                captures.append("chicken")
            elif defender_hen.isSquareSet(move.getTo()):
                self.hen.clearSquare(move.getTo())
                captures.append("chicken")

        attacker.setSquare(move.getTo())
        attacker.clearSquare(move.getFrom())
        piece_type.setSquare(move.getTo())
        piece_type.clearSquare(move.getFrom())

    def isGameOver(self):
        white_lion = BitBoard.BitBoard()
        white_lion.setBoard(self.lion.getBoard() & self.white.getBoard())
        if len(white_lion.allSetSquares()) == 0:
            return True

        black_lion = BitBoard.BitBoard()
        black_lion.setBoard(self.lion.getBoard() & self.black.getBoard())
        if len(black_lion.allSetSquares()) == 0:
            return True
        return False

    def hasWhiteWon(self):
        black_lion = BitBoard.BitBoard()
        black_lion.setBoard(self.lion.getBoard() & self.black.getBoard())
        if len(black_lion.allSetSquares()) == 0:
            return True
        return False

    def hasBlackWon(self):
        white_lion = BitBoard.BitBoard()
        white_lion.setBoard(self.lion.getBoard() & self.white.getBoard())
        if len(white_lion.allSetSquares()) == 0:
            return True
        return False

    def eval_func(self):
        eval = 0.0

        # piece value
        white_lion = BitBoard.BitBoard()
        white_lion.setBoard(self.lion.getBoard() & self.white.getBoard())
        temp = white_lion.allSetSquares()
        #eval = eval + len(temp) * 1000
        eval = eval + len(temp) * 100
        white_giraffe = BitBoard.BitBoard()
        white_giraffe.setBoard(self.giraffe.getBoard() & self.white.getBoard())
        temp = white_giraffe.allSetSquares()
        eval = eval + len(temp) * 5
        white_elephant = BitBoard.BitBoard()
        white_elephant.setBoard(self.elephant.getBoard() & self.white.getBoard())
        temp = white_elephant.allSetSquares()
        eval = eval + len(temp) * 3
        white_chicken = BitBoard.BitBoard()
        white_chicken.setBoard(self.chicken.getBoard() & self.white.getBoard())
        temp = white_chicken.allSetSquares()
        eval = eval + len(temp) * 1
        white_hen = BitBoard.BitBoard()
        white_hen.setBoard(self.hen.getBoard() & self.white.getBoard())
        temp = white_hen.allSetSquares()
        eval = eval + len(temp) * 7

        black_lion = BitBoard.BitBoard()
        black_lion.setBoard(self.lion.getBoard() & self.black.getBoard())
        temp = black_lion.allSetSquares()
        #eval = eval - len(temp) * 1000
        eval = eval - len(temp) * 100
        black_giraffe = BitBoard.BitBoard()
        black_giraffe.setBoard(self.giraffe.getBoard() & self.black.getBoard())
        temp = black_giraffe.allSetSquares()
        eval = eval - len(temp) * 5
        black_elephant = BitBoard.BitBoard()
        black_elephant.setBoard(self.elephant.getBoard() & self.black.getBoard())
        temp = black_elephant.allSetSquares()
        eval = eval - len(temp) * 3
        black_chicken = BitBoard.BitBoard()
        black_chicken.setBoard(self.chicken.getBoard() & self.black.getBoard())
        temp = black_chicken.allSetSquares()
        eval = eval - len(temp) * 1
        black_hen = BitBoard.BitBoard()
        black_hen.setBoard(self.hen.getBoard() & self.black.getBoard())
        temp = black_hen.allSetSquares()
        eval = eval - len(temp) * 7

        # capture value
        eval = eval + self.eval_captures(self.white_captures)

        eval = eval - self.eval_captures(self.black_captures)

        # freedom of units
        list = self.allpossibleMoves(True)
        for i in list:
            eval = eval + len(i)/4

        list = self.allpossibleMoves(False)
        for i in list:
            eval = eval - len(i)/4

        return eval

    def eval_win_loss(self):
        if self.hasWhiteWon():
            return 100
        elif self.hasBlackWon():
            return -100
        else:
            return 0

    def eval_captures(self, list):
        eval = 0.0
        for i in list:
            if i == "giraffe":
                eval = eval + 2.5
            elif i == "elephant":
                eval = eval + 1.5
            elif i == "chicken":
                eval = eval + 0.5
        return eval

    def get_Gamestate(self):
        list = []
        list.append(self.white.getBoard())
        list.append(self.black.getBoard())
        list.append(self.lion.getBoard())
        list.append(self.elephant.getBoard())
        list.append(self.giraffe.getBoard())
        list.append(self.chicken.getBoard())
        list.append(self.hen.getBoard())
        list.append(self.eval_func())
        list.append(self.white_captures)
        list.append(self.black_captures)
        return list

    def printBoard(self):
        white_lion = BitBoard.BitBoard()
        white_lion.setBoard(self.lion.getBoard() & self.white.getBoard())
        white_giraffe = BitBoard.BitBoard()
        white_giraffe.setBoard(self.giraffe.getBoard() & self.white.getBoard())
        white_elephant = BitBoard.BitBoard()
        white_elephant.setBoard(self.elephant.getBoard() & self.white.getBoard())
        white_chicken = BitBoard.BitBoard()
        white_chicken.setBoard(self.chicken.getBoard() & self.white.getBoard())
        white_hen = BitBoard.BitBoard()
        white_hen.setBoard(self.hen.getBoard() & self.white.getBoard())
        black_lion = BitBoard.BitBoard()
        black_lion.setBoard(self.lion.getBoard() & self.black.getBoard())
        black_giraffe = BitBoard.BitBoard()
        black_giraffe.setBoard(self.giraffe.getBoard() & self.black.getBoard())
        black_elephant = BitBoard.BitBoard()
        black_elephant.setBoard(self.elephant.getBoard() & self.black.getBoard())
        black_chicken = BitBoard.BitBoard()
        black_chicken.setBoard(self.chicken.getBoard() & self.black.getBoard())
        black_hen = BitBoard.BitBoard()
        black_hen.setBoard(self.hen.getBoard() & self.black.getBoard())

        for i in reversed(range(4)):
            for i2 in range(3):
                square = i * 3 + i2
                if white_lion.isSquareSet(square):
                    print("L", end=" ")
                elif white_giraffe.isSquareSet(square):
                    print("G", end=" ")
                elif white_elephant.isSquareSet(square):
                    print("E", end=" ")
                elif white_chicken.isSquareSet(square):
                    print("C", end=" ")
                elif white_hen.isSquareSet(square):
                    print("H", end=" ")
                elif black_lion.isSquareSet(square):
                    print("l", end=" ")
                elif black_giraffe.isSquareSet(square):
                    print("g", end=" ")
                elif black_elephant.isSquareSet(square):
                    print("e", end=" ")
                elif black_chicken.isSquareSet(square):
                    print("c", end=" ")
                elif black_hen.isSquareSet(square):
                    print("h", end=" ")
                else:
                    print("0", end=" ")
            print()

        print("White Captures:")
        for i in self.white_captures:
            print(i)

        print("Black Captures:")
        for i in self.black_captures:
            print(i)

if __name__ == '__main__':
    board = LionBoard()
    board.setBoard_start()

    print(board.getFen())

    for i in range(3):
        print(i)
    """list = board.allpossibleMoves(True)
    print("move lists len:",len(list))
    i2 = 1
    for i in list:
        print("List ", i2," Len:", len(i))
        i2 = i2 + 1
"""
    """board = LionBoard()
    board.setBoard_Fen("3/1l1/2L/C2/GgcEe")
    #board.setBoard_start()
    board.printBoard()
    print("")
    print(board.getFen())
    print("")
    board2 = LionBoard()
    board2.setBoard_Fen(board.getFen())
    board2.printBoard()"""

    """board = LionBoard()
    board.setBoard_start()
    board2 = LionBoard()
    board2.setBoard(board)
    print("1")
    board.printBoard()
    print("2")
    board2.printBoard()
    board.makeMove(True, 1, 3)
    print("")
    print("1")
    board.printBoard()
    print("2")
    board2.printBoard()"""

    """ 
    test = LionBoard()
    test.setBoard_start()
    test.printBoard()
    list = test.allpossibleMoves(True)
    for i in list:
        for i2 in i:
           i2.printMove()
    test.makeMove(True, 1, 3)
    test.printBoard()
    """

    """
    test.randomBoard()
    test.printBoard()
    print(test.eval_func())
    list = test.allpossibleMoves(True)
    for i in list:
        for i2 in i:
           i2.printMove()
    """

    """test = LionBoard()
    test.randomBoard()
    test.printBoard()
    test.makeRandomMove(True)
    test.printBoard()"""