import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import *

from Game import LionBoard, Move
from MonteCarlo import MCTS
from AlphaBeta import IterativeDeepening


def show_frame(frame):
    global current_frame
    try:
        current_frame.pack_forget()
    except NameError:
        pass
    frame.pack(expand=True, fill="both")
    frame.tkraise()
    current_frame = frame
    # frame.grid(row=0, column=0, sticky="nsew")


def on_select_white(event):
    global whiteplayer
    selected_item = white.get()
    whiteplayer = selected_item
    #black.grid(row=2, column=0, padx=10, pady=10)
    #black.pack()
    if whiteplayer == "Mini-Max":
        Mini_Max_1.pack()
    else:
        MCTS_1.pack()

def on_select_player_select_1(event):
    global player_1
    if whiteplayer == "Mini-Max":
        selected_item = Mini_Max_1.get()
    else:
        selected_item = MCTS_1.get()
    player_1 = selected_item
    #black.grid(row=2, column=0, padx=10, pady=10)
    black.pack()


def on_select_black(event):
    global blackplayer
    selected_item = black.get()
    blackplayer = selected_item
    #result_label.config(text=f"White: {whiteplayer} Black: {blackplayer}")
    #menu_button.grid(row=3, column=0, padx=10, pady=10)
    if blackplayer == "Mini-Max":
        Mini_Max_2.pack()
    else:
        MCTS_2.pack()

    #time_label.pack()
    #time_entry.pack()
    #iterations_label.pack()
    #iteratiions_entry.pack()
    #menu_button.pack()

def on_select_player_select_2(event):
    global player_2
    if blackplayer == "Mini-Max":
        selected_item = Mini_Max_2.get()
    else:
        selected_item = MCTS_2.get()
    player_2 = selected_item
    #black.grid(row=2, column=0, padx=10, pady=10)
    time_label.pack()
    time_entry.pack()
    iterations_label.pack()
    iteratiions_entry.pack()
    menu_button.pack()

"""def on_select_time(event):
    global time
    entry = time_entry.get()
    time = int(entry)
    #result_label.config(text=f"White: {whiteplayer} Black: {blackplayer}")
    #menu_button.grid(row=3, column=0, padx=10, pady=10)
    #menu_button.pack()
    iteratiions_entry.pack()


def on_select_iter(event):
    global iterations
    entry = iteratiions_entry.get()
    time = int(entry)
    #result_label.config(text=f"White: {whiteplayer} Black: {blackplayer}")
    #menu_button.grid(row=3, column=0, padx=10, pady=10)
    menu_button.pack()"""


def on_game_frame():
    global time
    global iterations
    entry = time_entry.get()
    time = int(entry)
    entry = iteratiions_entry.get()
    iterations = int(entry)
    show_frame(game_frame)
    add_text(f"Time is {time}")
    add_text(f"Iterations is {iterations}")
    add_text(f"White Player is {player_1}")
    add_text(f"Black Player is {player_2}")

# Function to add text to the scrolling window
def add_text(new_text):
    text_widget.insert(tk.END, new_text + "\n")
    #text_widget.update_idletasks()
    text_widget.update()


def game():
    sys.setrecursionlimit(15000)
    for i in range(0, iterations):
        board = LionBoard.LionBoard()
        board.setBoard_start()
        ID = IterativeDeepening.iterativeDeepeningAB()
        if i % 2 == 0:
            whiteTurn = True
        else:
            whiteTurn = False
        while not board.isGameOver():
            if whiteTurn:
                move = Move.Move()
                try:
                    match player_1:
                        case "Mini-Max":
                            eval, moves = ID.iterativeDeepening_AB(time, board, whiteTurn)
                            move = moves[0]
                        case "AB":
                            eval, moves = ID.iterativeDeepening_AB_TT(time, board, whiteTurn)
                            move = moves[0]
                        case "MCTS":
                            ResultNode = MCTS.MCTS(board, whiteTurn, time)
                            move = ResultNode.move
                        case "MCTS-MR":
                            ResultNode = MCTS.MCTS_MR(board, whiteTurn, time, 3)
                            move = ResultNode.move
                except TimeoutError:
                    pass
                board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                add_text(f"From: {move.getFrom()} To: {move.getTo()}")

                #ResultNode = MCTS.MCTS_Node
                #try:
                #    ResultNode = MCTS.MCTS_MR(board, whiteTurn, time, 3)
                #except TimeoutError:
                #    pass
                #board.makeMove(whiteTurn, ResultNode.move.getFrom(), ResultNode.move.getTo())
                #add_text(f"From: {ResultNode.move.getFrom()} To: {ResultNode.move.getTo()}")
            else:
                move = Move.Move()
                try:
                    match player_1:
                        case "Mini-Max":
                            eval, moves = ID.iterativeDeepening_AB(time, board, whiteTurn)
                            move = moves[0]
                        case "AB":
                            eval, moves = ID.iterativeDeepening_AB_TT(time, board, whiteTurn)
                            move = moves[0]
                        case "MCTS":
                            ResultNode = MCTS.MCTS(board, whiteTurn, time)
                            move = ResultNode.move
                        case "MCTS-MR":
                            ResultNode = MCTS.MCTS_MR(board, whiteTurn, time, 3)
                            move = ResultNode.move
                except TimeoutError:
                    pass
                board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                add_text(f"From: {move.getFrom()} To: {move.getTo()}")
                """ResultNode = MCTS.MCTS_Node
                try:
                    ResultNode = MCTS.MCTS_MR(board, whiteTurn, time, 3)
                except TimeoutError:
                    pass
                board.makeMove(whiteTurn, ResultNode.move.getFrom(), ResultNode.move.getTo())
                add_text(f"From: {ResultNode.move.getFrom()} To: {ResultNode.move.getTo()}")"""
            whiteTurn = not whiteTurn
        if board.hasWhiteWon():
            add_text("White has won")
        elif board.hasBlackWon():
            add_text("Black has won")


""""-----------------------------------------------------------------------------------------------------------"""
# the Root
root = tk.Tk()
root.geometry("700x350")
root.title("Simulator")
#root.grid_rowconfigure(0, weight=1)
#root.columnconfigure(0, weight=1)
""""-----------------------------------------------------------------------------------------------------------"""

""""-----------------------------------------------------------------------------------------------------------"""
# menu frame
menu_frame = tk.Frame(root)
#menu_frame.grid_rowconfigure(0, weight=1)
#menu_frame.grid_columnconfigure(0, weight=1)

menu_label = tk.Label(menu_frame, text="Menu Section")
#menu_button = tk.Button(menu_frame, text="Go to Game", command=lambda: show_frame(game_frame))
menu_button = tk.Button(menu_frame, text="Go to Game", command=on_game_frame)

time_label = tk.Label(menu_frame, text="Enter Time per Turn:")
time_entry = tk.Entry(menu_frame)
iterations_label = tk.Label(menu_frame, text="Enter Rounds to be played:")
iteratiions_entry = tk.Entry(menu_frame)

options = ["Mini-Max", "MCTS"]
Mini_Max_options = ["Mini-Max", "AB"]
MCTS_options = ["MCTS", "MCTS-MR"]

white = ttk.Combobox(menu_frame, values=options)
white.set("Select white Player")  # Set a default selection
white.bind("<<ComboboxSelected>>", on_select_white)

black = ttk.Combobox(menu_frame, values=options)
black.set("Select black Player")  # Set a default selection
black.bind("<<ComboboxSelected>>", on_select_black)

Mini_Max_1 = ttk.Combobox(menu_frame, values=Mini_Max_options)
Mini_Max_1.set("Select Mini_Max Variant")  # Set a default selection
Mini_Max_1.bind("<<ComboboxSelected>>", on_select_player_select_1)

Mini_Max_2 = ttk.Combobox(menu_frame, values=Mini_Max_options)
Mini_Max_2.set("Select Mini_Max Variant")  # Set a default selection
Mini_Max_2.bind("<<ComboboxSelected>>", on_select_player_select_2)

MCTS_1 = ttk.Combobox(menu_frame, values=MCTS_options)
MCTS_1.set("Select MCTS Variant")  # Set a default selection
MCTS_1.bind("<<ComboboxSelected>>", on_select_player_select_1)

MCTS_2 = ttk.Combobox(menu_frame, values=MCTS_options)
MCTS_2.set("Select MCTS Variant")  # Set a default selection
MCTS_2.bind("<<ComboboxSelected>>", on_select_player_select_2)

menu_label.pack()
white.pack()
#menu_label.grid(row=0, column=0, padx=10, pady=10)
#white.grid(row=1, column=0, padx=10, pady=10)
#menu_label.pack(side="top", fill="both", expand=True)
#menu_label.place(relx=.5, rely=.5,anchor= CENTER)
#white.pack(side="top", fill="both", expand=True)
#white.place(relx=0.5, rely=0.5, anchor= CENTER)
""""-----------------------------------------------------------------------------------------------------------"""

""""-----------------------------------------------------------------------------------------------------------"""
# game frame
game_frame = tk.Frame(root)
#game_frame.grid_rowconfigure(0, weight=1)
#game_frame.grid_columnconfigure(0, weight=1)

#result_label = tk.Label(game_frame, text="")
start_button = tk.Button(game_frame, text="Begin Game", command=game)
#start_button = tk.Button(game_frame, text="Begin Game", command=thread)
go_back_button = tk.Button(game_frame, text="Go Back", command=lambda: show_frame(menu_frame))

# Create a Text widget with vertical and horizontal scrollbars
text_widget = scrolledtext.ScrolledText(game_frame, wrap=tk.WORD, width=80, height=20)

#result_label.grid(row=0, column=0, padx=10, pady=10)
start_button.pack()
text_widget.pack()
go_back_button.pack()
""""-----------------------------------------------------------------------------------------------------------"""

""""-----------------------------------------------------------------------------------------------------------"""
# The Loop
show_frame(menu_frame)
root.mainloop()
""""-----------------------------------------------------------------------------------------------------------"""
