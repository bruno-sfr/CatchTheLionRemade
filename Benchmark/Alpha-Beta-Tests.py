import time

from AlphaBeta import AlphaBeta
from Game import LionBoard

def Possible_Pos():
    board = LionBoard.LionBoard()
    board.setBoard_start()
    print(board.getFen())

    list = board.allpossibleMoves_BigList(True)
    for i in list:
        new_Board = LionBoard.LionBoard()
        new_Board.setBoard_start()
        new_Board.makeMove(True, i.getFrom(), i.getTo())
        print(f"\"{new_Board.getFen()}\"")

        """ second_list = new_Board.allpossibleMoves_BigList(False)
        for i2 in second_list:
            new_new_Board = LionBoard.LionBoard()
            new_new_Board.setBoard_Fen(new_Board.getFen())
            new_new_Board.makeMove(False, i2.getFrom(), i2.getTo())

            third_list = new_new_Board.allpossibleMoves_BigList(True)
            for i3 in third_list:
                new_3_Board = LionBoard.LionBoard()
                new_3_Board.setBoard_Fen(new_new_Board.getFen())
                new_3_Board.makeMove(True, i3.getFrom(), i3.getTo())

                forth_list = new_3_Board.allpossibleMoves_BigList(False)
                for i4 in forth_list:
                    new_4_Board = LionBoard.LionBoard()
                    new_4_Board.setBoard_Fen(new_3_Board.getFen())
                    new_4_Board.makeMove(False, i4.getFrom(), i4.getTo())
                    print(new_4_Board.getFen())"""
                    #print(f"\"{new_4_Board.getFen()}\"")
            #new_new_Board.printBoard()
            #print("")
            #print(new_new_Board.getFen())

def AB_VS_AB():
    """Positions = ["e1g/1cl/1CL/G1E/", "e1g/lc1/1CL/G1E/", "el1/1cg/1CL/G1E/", "elg/111/1cL/G1E/c", "e1g/1cl/LC1/G1E/",
                 "e1g/lc1/LC1/G1E/", "el1/1cg/LC1/G1E/", "elg/111/Lc1/G1E/c", "e1g/1cl/GC1/1LE/", "e1g/lc1/GC1/1LE/",
                 "el1/1cg/GC1/1LE/", "elg/111/Gc1/1LE/c", "e1g/1Cl/111/GLE/C", "e1g/1l1/111/GLE/cC", "e1g/lC1/111/GLE/C",
                 "el1/1Cg/111/GLE/C", "1lg/1e1/111/GLE/cC"]"""
    Positions_0 = ["elg/1c1/1C1/GLE/"]
    Positions = ["elg/1c1/1CL/G1E/", "elg/1c1/LC1/G1E/", "elg/1c1/GC1/1LE/", "elg/1C1/111/GLE/C"]
    #Positions = ["e1g/lc1/1CL/G1E/", "el1/1cg/1CL/G1E/", "elg/111/1cL/G1E/c", "e1g/1cl/LC1/G1E/","el1/1cg/LC1/G1E/",
    #             "elg/111/Lc1/G1E/c", "e1g/1cl/GC1/1LE/", "el1/1cg/GC1/1LE/", "elg/111/Gc1/1LE/c", "e1g/1Cl/111/GLE/C",
    #             "e1g/1l1/111/GLE/cC", "e1g/lC1/111/GLE/C", "1lg/1e1/111/GLE/cC"]

    """Positions = []
    with open('./Board_Positions.txt', 'r') as file:
        # Read all lines from the file into an array
        Positions = file.readlines()"""

    """for pos in Positions:
        board = LionBoard.LionBoard()
        board.setBoard_Fen(pos)
        board.printBoard()"""

    A_Depth = 9
    B_Depth = 10
    A_Wins = 0
    B_Wins = 0
    max_turns = 100

    for pos in Positions:
        print("New Position:", pos)
        for i in range(2):
            board = LionBoard.LionBoard()
            board.setBoard_Fen(pos)
            whiteTurn = False
            turns = 0
            if i == 0:
                print("Even Play")
                while not board.isGameOver():
                    if whiteTurn:
                        evalAB, move = AlphaBeta.alpha_beta_simple(A_Depth, board, whiteTurn)
                        #evalAB, move, temp = AlphaBeta.alpha_beta_quiescence_simple(A_Depth, board, whiteTurn)
                        #evalAB, moves, evals = AlphaBeta.alpha_beta_quiescence_allMoves_simple(A_Depth, board, whiteTurn)
                        #move = moves[0]
                        board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    else:
                        evalAB, move = AlphaBeta.alpha_beta_simple(B_Depth, board, whiteTurn)
                        #evalAB, move, temp = AlphaBeta.alpha_beta_quiescence_simple(B_Depth, board, whiteTurn)
                        board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    whiteTurn = not whiteTurn

                    turns = turns + 1
                    if turns > max_turns:
                        break

                if board.hasWhiteWon():
                    A_Wins = A_Wins + 1
                elif board.hasBlackWon():
                    B_Wins = B_Wins + 1
                else:
                    B_Wins = B_Wins + 0.5
                    A_Wins = A_Wins + 0.5
            else:
                print("Uneven Play")
                while not board.isGameOver():
                    if whiteTurn:
                        evalAB, move = AlphaBeta.alpha_beta_simple(B_Depth, board, whiteTurn)
                        #evalAB, move, temp = AlphaBeta.alpha_beta_quiescence_simple(B_Depth, board, whiteTurn)
                        board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    else:
                        evalAB, move = AlphaBeta.alpha_beta_simple(A_Depth, board, whiteTurn)
                        #evalAB, move, temp = AlphaBeta.alpha_beta_quiescence_simple(A_Depth, board, whiteTurn)
                        #evalAB, moves, evals = AlphaBeta.alpha_beta_quiescence_allMoves_simple(A_Depth, board, whiteTurn)
                        #move = moves[0]
                        board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    whiteTurn = not whiteTurn

                    turns = turns + 1
                    if turns > max_turns:
                        break

                if board.hasWhiteWon():
                    B_Wins = B_Wins + 1
                elif board.hasBlackWon():
                    A_Wins = A_Wins + 1
                else:
                    B_Wins = B_Wins + 0.5
                    A_Wins = A_Wins + 0.5
        print(f"AB-{A_Depth} {A_Wins} : {B_Wins} AB-{B_Depth}")

def Mate_in_Test():
    depth = 5
    boards = ["eg1/lc1/1CL/G1E/", "eg1/1l1/GE1/1L1/cC", "1l1/G2/L1g/2E/cCE", "eg1/lc1/1CL/G1E/", "1g1/G1l/3/1LE/cC"]
    board = LionBoard.LionBoard()

    for fen in boards:
        print(fen)
        board.setBoard_Fen(fen)
        #evalAB, move = AlphaBeta.alpha_beta_simple(depth, board, True)#
        evalAB, moves, evals = AlphaBeta.alpha_beta_allMoves_simple(depth, board, True)
        #evalAB, move = AlphaBeta.NegaMax(float('-inf'), float('inf'), depth, board, True)
        #evalAB, move, temp = AlphaBeta.alpha_beta_quiescence_simple(depth, board, True)
        #evalAB, moves, evals = AlphaBeta.alpha_beta_quiescence_allMoves_simple(depth, board, True)
        print("Eval =", evalAB)
        moves[0].printMove()
        #move.printMove()
        print("")

def eval_varianz_test():
    board = LionBoard.LionBoard()
    board.setBoard_start()
    Depth = 6
    for i in range(Depth):
        print("Depth:", i+1)
        print("Quiet:")
        evalAB, moves, evals = AlphaBeta.alpha_beta_quiescence_allMoves_simple((i+1), board, True)
        print("Eval:", evalAB)
        for move in moves:
            move.printMove()
        print("--------")
        print("Normal:")
        evalAB, moves, evals = AlphaBeta.alpha_beta_allMoves_simple((i+1), board, True)
        print("Eval:", evalAB)
        for move in moves:
            move.printMove()
        print("")

def test_allMoves():
    boards = ["eg1/lc1/1CL/G1E/", "eg1/1l1/GE1/1L1/cC", "1l1/G2/L1g/2E/cCE", "eg1/lc1/1CL/G1E/", "1g1/G1l/3/1LE/cC",
              "1l1/Ge1/L1g/2E/cC", "1l1/Gg1/1Ee/2L/cC", "el1/1c1/GCg/1LE/", "1l1/1e1/1Gg/1LE/Cc", "lc1/E2/3/L"]
    #boards = ["11g/11l/Lce/1CG/e"]
    whiteTurn = True

    for board in boards:
        lionboard = LionBoard.LionBoard()
        lionboard.setBoard_Fen(board)
        lionboard.printBoard()
        print("")
        list_a = lionboard.allpossibleMoves_BigList(whiteTurn)
        list_b = lionboard.allpossibleMoves_baier_biglist(whiteTurn)
        print("List A")
        for move in list_a:
            move.printMove()
        print("List B")
        for move in list_b:
            move.printMove()
        print("")
        for move in list_a:
            move_exists = False
            for move_b in list_b:
                if move.equals(move_b):
                    move_exists = True
                    break
            if move_exists:
                continue
            else:
                print("Faulty Move detected")
                move.printMove()
                return
    print("Test passed")


def test_allMoves_random():
    #boards = ["eg1/lc1/1CL/G1E/", "eg1/1l1/GE1/1L1/cC", "1l1/G2/L1g/2E/cCE", "eg1/lc1/1CL/G1E/", "1g1/G1l/3/1LE/cC",
    #          "1l1/Ge1/L1g/2E/cC", "1l1/Gg1/1Ee/2L/cC", "el1/1c1/GCg/1LE/", "1l1/1e1/1Gg/1LE/Cc", "lc1/E2/3/L"]
    #boards = ["1l1/1e1/1Gg/1LE/Cc"]
    whiteTurn = True

    for i in range(1000):
        lionboard = LionBoard.LionBoard()
        lionboard.randomBoard()
        print(lionboard.getFen())
        print("")
        list_a = lionboard.allpossibleMoves_BigList(whiteTurn)
        list_b = lionboard.allpossibleMoves_baier_biglist(whiteTurn)

        if len(list_a) != len(list_b):
            print("Length mismatch!")
            return

        """print("List A")
        for move in list_a:
            move.printMove()
        print("List B")
        for move in list_b:
            move.printMove()
        print("")"""
        for move in list_a:
            move_exists = False
            for move_b in list_b:
                if move.equals(move_b):
                    move_exists = True
                    break
            if move_exists:
                continue
            else:
                print("Faulty Move detected")
                move.printMove()
                return
    print("Test passed")

def PV_Test():
    board = LionBoard.LionBoard()
    boards = ["eg1/lc1/1CL/G1E/", "eg1/1l1/GE1/1L1/cC", "1l1/G2/L1g/2E/cCE", "eg1/lc1/1CL/G1E/", "1g1/G1l/3/1LE/cC",
              "1l1/Ge1/L1g/2E/cC", "1l1/Gg1/1Ee/2L/cC", "el1/1c1/GCg/1LE/", "1l1/1e1/1Gg/1LE/Cc"]
    Depth = 6

    for pos in boards:
        print("")
        board.setBoard_Fen(pos)
        whiteTurn = True
        for i in reversed(range(Depth + 1)):
            if i == 0:
                break
            print("Depth ", i)
            evalAB, moves, evals = AlphaBeta.alpha_beta_quiescence_allMoves_simple(i, board, whiteTurn)
            print("Eval:", evalAB)
            for move in moves:
                move.printMove()
            print("----Making-Move----")
            board.makeMove(whiteTurn, moves[0].getFrom(), moves[0].getTo())
            whiteTurn = not whiteTurn
            if board.isGameOver():
                break

def Quiet_Test():
    board = LionBoard.LionBoard()
    board.setBoard_Fen("e1l/Gcg/EC1/1L1")
    board.printBoard()
    Depth = 5
    print("")

    print("Quiet:")
    evalAB, moves, evals = AlphaBeta.alpha_beta_quiescence_allMoves_simple(Depth, board, True)
    print("Eval:",evalAB)
    for i in moves:
        i.printMove()
    print("--------")
    print("Normal:")
    evalAB, moves, evals = AlphaBeta.alpha_beta_allMoves_simple(Depth, board, True)
    print("Eval:", evalAB)
    for i in moves:
        i.printMove()
    print("")

def Quiet_Search_Test():
    board = LionBoard.LionBoard()
    board.setBoard_Fen("e1l/Gcg/ECL/3")
    eval = AlphaBeta.quiescence_search(float('-inf'), float('inf'), board, False)
    print("Eval:",eval)

if __name__ == '__main__':
    #Possible_Pos()
    AB_VS_AB()
    #Mate_in_Test()
    #PV_Test()
    #Quiet_Test()
    #eval_varianz_test()
    #Quiet_Search_Test()
    #test_allMoves()
    #test_allMoves_random()