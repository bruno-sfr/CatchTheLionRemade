from GUI import The_GUI
from Game import LionBoard

def HumanVsHuman():
    board = LionBoard.LionBoard()
    board.setBoard_start()
    whiteTurn = True
    while True:
        board.printBoard()
        print("WhiteTurn:", whiteTurn)
        print("From?")
        __from = input()
        temp_from = str(__from)
        if temp_from == "c" or temp_from == "g" or temp_from == "e":
            _from = temp_from
        else:
            _from = int(__from)
        print("To?")
        _to = int(input())
        print(board.makeMove(whiteTurn, _from, _to))
        print("Has White won?", board.hasWhiteWon())
        whiteTurn = not whiteTurn

if __name__ == '__main__':
    GUI = The_GUI.GUI()
    GUI.Start_GUI()
