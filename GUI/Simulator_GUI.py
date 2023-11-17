import math
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt

from PIL import Image, ImageTk
from Game import LionBoard, Move
from AlphaBeta import IterativeDeepening
from MonteCarlo import MCTS


class SimGUI:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.canvas = tk.Canvas(self.frame, width=1000, height=700)
        self.canvas.pack()
        self.images = []

        self.white_player = ""
        self.black_player = ""
        self.time = 0
        self.iterations = 0
        self.white_wins = 0
        self.white_wins_list = [0]
        self.black_wins = 0
        self.black_wins_list = [0]

        img = Image.open("../GUI_Resources/Catch_The_Lion_Simple.png")
        resized_image = img.resize((1000, 700))
        self.images.append(ImageTk.PhotoImage(resized_image))
        self.canvas.create_image(500, 350, image=self.images[-1])

        self.text_widget = scrolledtext.ScrolledText(self.canvas, wrap=tk.WORD)
        options = ["Mini-Max", "AB", "MCTS", "MCTS-MR"]
        self.white = ttk.Combobox(self.canvas, values=options)
        self.white.set("Select white Player")  # Set a default selection
        self.black = ttk.Combobox(self.canvas, values=options)
        self.black.set("Select black Player")  # Set a default selection
        #white.bind("<<ComboboxSelected>>", on_select_white)
        self.time_label = tk.Label(self.canvas, text="Enter Time per Turn:")
        self.time_entry = tk.Entry(self.canvas)
        self.iterations_label = tk.Label(self.canvas, text="Enter Rounds to be played:")
        self.iterations_entry = tk.Entry(self.canvas)
        self.begin_button = tk.Button(self.canvas, text="Begin Simulation", command=self.Begin, anchor="center")
        self.plot_button = tk.Button(self.canvas, text="Plot Simulation", command=self.plot_result, anchor="center")
        self.round_Label = tk.Label(self.canvas, text="Rounds to be played")

        self.window_1 = self.canvas.create_window(350, 350, width=600, height=600, window=self.text_widget)
        self.window_2 = self.canvas.create_window(825, 100, width=200, height=30, window=self.white)
        self.window_3 = self.canvas.create_window(825, 150, width=200, height=30, window=self.black)
        self.window_4 = self.canvas.create_window(825, 200, width=200, height=30, window=self.time_label)
        self.window_5 = self.canvas.create_window(825, 225, width=200, height=30, window=self.time_entry)
        self.window_6 = self.canvas.create_window(825, 275, width=200, height=30, window=self.iterations_label)
        self.window_7 = self.canvas.create_window(825, 300, width=200, height=30, window=self.iterations_entry)
        self.window_8 = self.canvas.create_window(825, 350, width=200, height=30, window=self.begin_button)
        self.window_9 = self.canvas.create_window(825, 400, width=200, height=30, window=self.plot_button)
        self.window_10 = self.canvas.create_window(350, 27, width=200, height=30, window=self.round_Label)
        self.canvas.itemconfig(self.window_10, state="hidden")

    def add_text(self, new_text):
        self.text_widget.insert(tk.END, new_text + "\n")
        self.text_widget.update()

    def Begin(self):
        #self.add_text("Hello")
        self.white_player = self.white.get()
        self.black_player = self.black.get()
        self.time = int(self.time_entry.get())
        self.iterations = int(self.iterations_entry.get())
        self.white_wins = 0
        self.white_wins_list = [0]
        self.black_wins = 0
        self.black_wins_list = [0]
        self.game()

    def game(self):
        sys.setrecursionlimit(15000)
        self.canvas.itemconfig(self.window_10, state="normal")
        for i in range(0, self.iterations):
            self.round_Label.config(text=f"Round {i + 1} of {self.iterations}")
            self.canvas.update()
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
                        match self.white_player:
                            case "Mini-Max":
                                eval, moves = ID.iterativeDeepening_AB(self.time, board, whiteTurn)
                                move = moves[0]
                            case "AB":
                                eval, moves = ID.iterativeDeepening_AB_TT(self.time, board, whiteTurn)
                                move = moves[0]
                            case "MCTS":
                                ResultNode = MCTS.MCTS(board, whiteTurn, self.time)
                                move = ResultNode.move
                            case "MCTS-MR":
                                ResultNode = MCTS.MCTS_MR(board, whiteTurn, self.time, 3)
                                move = ResultNode.move
                    except TimeoutError:
                        pass
                    board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    self.add_text(f"From: {move.getFrom()} To: {move.getTo()}")
                else:
                    move = Move.Move()
                    try:
                        match self.black_player:
                            case "Mini-Max":
                                eval, moves = ID.iterativeDeepening_AB(self.time, board, whiteTurn)
                                move = moves[0]
                            case "AB":
                                eval, moves = ID.iterativeDeepening_AB_TT(self.time, board, whiteTurn)
                                move = moves[0]
                            case "MCTS":
                                ResultNode = MCTS.MCTS(board, whiteTurn, self.time)
                                move = ResultNode.move
                            case "MCTS-MR":
                                ResultNode = MCTS.MCTS_MR(board, whiteTurn, self.time, 3)
                                move = ResultNode.move
                    except TimeoutError:
                        pass
                    board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    self.add_text(f"From: {move.getFrom()} To: {move.getTo()}")
                whiteTurn = not whiteTurn
            if board.hasWhiteWon():
                self.add_text("White has won")
                self.white_wins = self.white_wins + 1
            elif board.hasBlackWon():
                self.add_text("Black has won")
                self.black_wins = self.black_wins + 1
            self.white_wins_list.append(self.white_wins)
            self.black_wins_list.append(self.black_wins)

    def plot_result(self):
        x = range(0, self.iterations + 1)
        #x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
        #plt.xticks(x_list)

        plt.plot(x, self.white_wins_list, label=self.white_player)
        plt.plot(x, self.black_wins_list, label=self.black_player)
        plt.xlabel("Rounds")
        plt.ylabel("Wins")
        plt.title(f"Comparison {self.white_player} vs {self.black_player} Time {self.time}")
        plt.legend()
        plt.savefig(f"../Resources/Benchmark_GUI_{self.white_player}_vs_{self.black_player}_{self.time}s.png")
        #plt.show()

        self.plot_canvas = tk.Canvas(self.frame, width=1000, height=700)
        img = Image.open(f"../Resources/Benchmark_GUI_{self.white_player}_vs_{self.black_player}_{self.time}s.png")
        resized_image = img.resize((933, 700))
        self.images.append(ImageTk.PhotoImage(resized_image))
        self.plot_canvas.create_image(466, 350, image=self.images[-1])
        self.canvas.pack_forget()
        self.plot_canvas.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")

    Lion_frame = tk.Frame(root)
    GUI = SimGUI(root, Lion_frame)
    Lion_frame.pack(expand=True, fill="both")
    Lion_frame.tkraise()
    root.mainloop()
