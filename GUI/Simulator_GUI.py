import math
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt

from PIL import Image, ImageTk
from Game import LionBoard, Move
from AlphaBeta import IterativeDeepening
from MonteCarlo import MCTS_Solvers


class SimGUI:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.canvas = tk.Canvas(self.frame, width=1000, height=700)
        self.canvas.pack()
        self.images = []

        self.white_player = ""
        self.white_Depth = 0
        self.white_Threshold = 0
        self.black_Depth = 0
        self.black_Threshold = 0
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
        options = ["MiniMax", "Alpha-Beta", "Alpha-Beta with TT", "MTD(f)",
                   "MCTS-Solver", "MCTS-MR", "MCTS-MS", "MCTS-MB"]
        self.white = ttk.Combobox(self.canvas, values=options)
        self.white.set("Select white Player")  # Set a default selection
        self.white.bind("<<ComboboxSelected>>", self.white_select)
        self.black = ttk.Combobox(self.canvas, values=options)
        self.black.set("Select black Player")  # Set a default selection
        self.black.bind("<<ComboboxSelected>>", self.black_select)
        self.time_label = tk.Label(self.canvas, text="Enter Time per Turn:")
        self.time_entry = tk.Entry(self.canvas)
        self.iterations_label = tk.Label(self.canvas, text="Enter Rounds to be played:")
        self.iterations_entry = tk.Entry(self.canvas)
        self.begin_button = tk.Button(self.canvas, text="Begin Simulation", command=self.Begin, anchor="center")
        self.plot_button = tk.Button(self.canvas, text="Plot Simulation", command=self.plot_result, anchor="center")
        self.round_Label = tk.Label(self.canvas, text="Rounds to be played")
        self.Game_state_Label = tk.Label(self.canvas, text="Game State")

        self.window_1 = self.canvas.create_window(350, 350, width=600, height=600, window=self.text_widget)
        self.window_2 = self.canvas.create_window(825, 100, width=200, height=30, window=self.white)
        self.window_3 = self.canvas.create_window(825, 150, width=200, height=30, window=self.black)
        self.window_4 = self.canvas.create_window(825, 200, width=200, height=30, window=self.time_label)
        self.window_5 = self.canvas.create_window(825, 225, width=200, height=30, window=self.time_entry)
        self.window_6 = self.canvas.create_window(825, 275, width=200, height=30, window=self.iterations_label)
        self.window_7 = self.canvas.create_window(825, 300, width=200, height=30, window=self.iterations_entry)
        self.window_8 = self.canvas.create_window(825, 350, width=200, height=30, window=self.begin_button)
        self.window_9 = self.canvas.create_window(825, 400, width=200, height=30, window=self.plot_button)
        self.window_10 = self.canvas.create_window(350, 27, width=160, height=30, window=self.round_Label)
        self.window_11 = self.canvas.create_window(350, 670, width=300, height=30, window=self.Game_state_Label)

        self.canvas.itemconfig(self.window_10, state="hidden")
        self.canvas.itemconfig(self.window_11, state="hidden")

        self.white_select_1 = self.canvas.create_window(747, 450, width=150, height=30)
        self.white_select_2 = self.canvas.create_window(747, 500, width=150, height=30)
        self.white_select_3 = self.canvas.create_window(747, 525, width=150, height=30)
        self.white_select_4 = self.canvas.create_window(747, 575, width=150, height=30)
        self.white_select_5 = self.canvas.create_window(747, 600, width=150, height=30)
        self.canvas.itemconfig(self.white_select_1, state="hidden")
        self.canvas.itemconfig(self.white_select_2, state="hidden")
        self.canvas.itemconfig(self.white_select_3, state="hidden")
        self.canvas.itemconfig(self.white_select_4, state="hidden")
        self.canvas.itemconfig(self.white_select_5, state="hidden")

        self.black_select_1 = self.canvas.create_window(903, 450, width=150, height=30)
        self.black_select_2 = self.canvas.create_window(903, 500, width=150, height=30)
        self.black_select_3 = self.canvas.create_window(903, 525, width=150, height=30)
        self.black_select_4 = self.canvas.create_window(903, 575, width=150, height=30)
        self.black_select_5 = self.canvas.create_window(903, 600, width=150, height=30)
        self.canvas.itemconfig(self.black_select_1, state="hidden")
        self.canvas.itemconfig(self.black_select_2, state="hidden")
        self.canvas.itemconfig(self.black_select_3, state="hidden")
        self.canvas.itemconfig(self.black_select_4, state="hidden")
        self.canvas.itemconfig(self.black_select_5, state="hidden")

    def white_select(self, event):
        self.white_player = self.white.get()
        self.white_text = tk.Label(self.canvas, text=f"{self.white_player}")
        self.canvas.itemconfig(self.white_select_1, state="normal", window=self.white_text)
        match self.white_player:
            case "MCTS-MR" | "MCTS-MB":
                self.white_parameter_1 = tk.Label(self.canvas, text=f"Depth:")
                self.white_parameter_1_entry = tk.Entry(self.canvas)
                self.canvas.itemconfig(self.white_select_2, state="normal", window=self.white_parameter_1)
                self.canvas.itemconfig(self.white_select_3, state="normal", window=self.white_parameter_1_entry)
                self.canvas.itemconfig(self.white_select_4, state="hidden")
                self.canvas.itemconfig(self.white_select_5, state="hidden")
            case "MCTS-MS":
                self.white_parameter_1 = tk.Label(self.canvas, text=f"Depth:")
                self.white_parameter_1_entry = tk.Entry(self.canvas)
                self.white_parameter_2 = tk.Label(self.canvas, text=f"Threshold:")
                self.white_parameter_2_entry = tk.Entry(self.canvas)
                self.canvas.itemconfig(self.white_select_2, state="normal", window=self.white_parameter_1)
                self.canvas.itemconfig(self.white_select_3, state="normal", window=self.white_parameter_1_entry)
                self.canvas.itemconfig(self.white_select_4, state="normal", window=self.white_parameter_2)
                self.canvas.itemconfig(self.white_select_5, state="normal", window=self.white_parameter_2_entry)
            case _:
                # all ABs
                self.white_parameter = tk.Label(self.canvas, text=f"No additional")
                self.white_parameter_2 = tk.Label(self.canvas, text=f"Parameters")
                self.canvas.itemconfig(self.white_select_2, state="normal", window=self.white_parameter)
                self.canvas.itemconfig(self.white_select_3, state="normal", window=self.white_parameter_2)
                self.canvas.itemconfig(self.white_select_4, state="hidden")
                self.canvas.itemconfig(self.white_select_5, state="hidden")

    def black_select(self, event):
        self.black_player = self.black.get()
        self.black_text = tk.Label(self.canvas, text=f"{self.black_player}")
        self.canvas.itemconfig(self.black_select_1, state="normal", window=self.black_text)
        match self.black_player:
            case "MCTS-MR" | "MCTS-MB":
                self.black_parameter_1 = tk.Label(self.canvas, text=f"Depth:")
                self.black_parameter_1_entry = tk.Entry(self.canvas)
                self.canvas.itemconfig(self.black_select_2, state="normal", window=self.black_parameter_1)
                self.canvas.itemconfig(self.black_select_3, state="normal", window=self.black_parameter_1_entry)
                self.canvas.itemconfig(self.black_select_4, state="hidden")
                self.canvas.itemconfig(self.black_select_5, state="hidden")
            case "MCTS-MS":
                self.black_parameter_1 = tk.Label(self.canvas, text=f"Depth:")
                self.black_parameter_1_entry = tk.Entry(self.canvas)
                self.black_parameter_2 = tk.Label(self.canvas, text=f"Threshold:")
                self.black_parameter_2_entry = tk.Entry(self.canvas)
                self.canvas.itemconfig(self.black_select_2, state="normal", window=self.black_parameter_1)
                self.canvas.itemconfig(self.black_select_3, state="normal", window=self.black_parameter_1_entry)
                self.canvas.itemconfig(self.black_select_4, state="normal", window=self.black_parameter_2)
                self.canvas.itemconfig(self.black_select_5, state="normal", window=self.black_parameter_2_entry)
            case _:
                # all ABs
                self.black_parameter = tk.Label(self.canvas, text=f"No additional")
                self.black_parameter_2 = tk.Label(self.canvas, text=f"Parameters")
                self.canvas.itemconfig(self.black_select_2, state="normal", window=self.black_parameter)
                self.canvas.itemconfig(self.black_select_3, state="normal", window=self.black_parameter_2)
                self.canvas.itemconfig(self.black_select_4, state="hidden")
                self.canvas.itemconfig(self.black_select_5, state="hidden")


    def add_text(self, new_text):
        self.text_widget.insert(tk.END, new_text + "\n")
        self.text_widget.yview(tk.END)
        self.text_widget.update()

    def Begin(self):
        #self.add_text("Hello")
        self.time = int(self.time_entry.get())
        self.iterations = int(self.iterations_entry.get())
        self.white_wins = 0
        self.white_wins_list = [0]
        self.black_wins = 0
        self.black_wins_list = [0]
        self.canvas.itemconfig(self.window_10, state="normal")
        self.canvas.itemconfig(self.window_11, state="normal")
        match self.white_player:
            case "MCTS-MR" | "MCTS-MB":
                self.white_Depth = int(self.white_parameter_1_entry.get())
            case "MCTS-MS":
                self.white_Depth = int(self.white_parameter_1_entry.get())
                self.white_Threshold = int(self.white_parameter_2_entry.get())

        match self.black_player:
            case "MCTS-MR" | "MCTS-MB":
                self.black_Depth = int(self.black_parameter_1_entry.get())
            case "MCTS-MS":
                self.black_Depth = int(self.black_parameter_1_entry.get())
                self.black_Threshold = int(self.black_parameter_2_entry.get())
        self.Game_state_Label.config(
            text=f"{self.white_player} 0 : 0 {self.black_player}")
        self.game()

    def game(self):
        #sys.setrecursionlimit(15000)
        max_turns = 100
        #max_turns = 50
        for i in range(0, self.iterations):
            turns = 0
            self.round_Label.config(text=f"Round {i + 1} of {self.iterations}")
            self.canvas.update()
            board = LionBoard.LionBoard()
            board.setBoard_start()
            ID = IterativeDeepening.iterativeDeepeningAB()
            MTD = IterativeDeepening.iterativeDeepeningMTD()
            if i % 2 == 0:
                whiteTurn = True
            else:
                whiteTurn = False
            while not board.isGameOver():
                if whiteTurn:
                    move = Move.Move()
                    try:
                        match self.white_player:
                            case "MiniMax":
                                eval, move, depth = ID.iterativeDeepening_MM(self.time, board, whiteTurn)
                            case "Alpha-Beta":
                                eval, move, depth = ID.iterativeDeepening_AB(self.time, board, whiteTurn)
                                #move = move
                            case "Alpha-Beta with TT":
                                eval, move, depth = ID.iterativeDeepening_AB_TT(self.time, board, whiteTurn)
                                #move = moves[0]
                            case "MTD(f)":
                                eval, move, depth = MTD.iterativeDeepening_MTD(self.time, board, whiteTurn)
                                #move = moves[0]
                            case "MCTS-Solver":
                                ResultNode = MCTS_Solvers.MCTS_Solver_Run(board, whiteTurn, self.time)
                                move = ResultNode.move
                            case "MCTS-MR":
                                ResultNode = MCTS_Solvers.MCTS_MR_Run(board, whiteTurn, self.time, self.white_Depth)
                                move = ResultNode.move
                            case "MCTS-MS":
                                ResultNode = MCTS_Solvers.MCTS_MS_Run(board, whiteTurn, self.time, self.white_Threshold, self.white_Depth)
                                move = ResultNode.move
                            case "MCTS-MB":
                                ResultNode = MCTS_Solvers.MCTS_MB_Run(board, whiteTurn, self.time, self.white_Depth)
                                move = ResultNode.move
                    except TimeoutError:
                        print("Am i the problem?")
                        pass
                    board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    self.add_text(f"From: {move.getFrom()} To: {move.getTo()}")
                else:
                    move = Move.Move()
                    try:
                        match self.black_player:
                            case "MiniMax":
                                eval, moves, depth = ID.iterativeDeepening_MM(self.time, board, whiteTurn)
                                move = moves[0]
                            case "Alpha-Beta":
                                eval, move, depth = ID.iterativeDeepening_AB(self.time, board, whiteTurn)
                                #move = moves
                            case "Alpha-Beta with TT":
                                eval, move, depth = ID.iterativeDeepening_AB_TT(self.time, board, whiteTurn)
                                #move = moves[0]
                            case "MTD(f)":
                                eval, move, depth = MTD.iterativeDeepening_MTD(self.time, board, whiteTurn)
                                #move = moves[0]
                            case "MCTS-Solver":
                                ResultNode = MCTS_Solvers.MCTS_Solver_Run(board, whiteTurn, self.time)
                                move = ResultNode.move
                            case "MCTS-MR":
                                ResultNode = MCTS_Solvers.MCTS_MR_Run(board, whiteTurn, self.time, self.black_Depth)
                                move = ResultNode.move
                            case "MCTS-MS":
                                ResultNode = MCTS_Solvers.MCTS_MS_Run(board, whiteTurn, self.time, self.black_Threshold, self.black_Depth)
                                move = ResultNode.move
                            case "MCTS-MB":
                                ResultNode = MCTS_Solvers.MCTS_MB_Run(board, whiteTurn, self.time, self.black_Depth)
                                move = ResultNode.move
                    except TimeoutError:
                        #print("Am i the problem?")
                        pass
                    board.makeMove(whiteTurn, move.getFrom(), move.getTo())
                    self.add_text(f"From: {move.getFrom()} To: {move.getTo()}")
                whiteTurn = not whiteTurn
                turns = turns + 1
                #self.add_text(f"turn: {turns}")
                if turns > max_turns:
                    break
            if board.hasWhiteWon():
                self.add_text(f"{self.white_player} has won")
                self.white_wins = self.white_wins + 1
            elif board.hasBlackWon():
                self.add_text(f"{self.black_player} has won")
                self.black_wins = self.black_wins + 1
            else:
                self.add_text(f"Time out Draw")
                self.black_wins = self.black_wins + 0.5
                self.white_wins = self.white_wins + 0.5
            self.white_wins_list.append(self.white_wins)
            self.black_wins_list.append(self.black_wins)
            #self.add_text(f"{self.white_player} {self.white_wins} : {self.black_wins} {self.black_player}")
            self.Game_state_Label.config(text=f"{self.white_player} {self.white_wins} : {self.black_wins} {self.black_player}")
        self.round_Label.config(text="Finished")

    def plot_result(self):
        x = range(0, self.iterations + 1)
        #x_list = range(math.floor(min(x)), math.ceil(max(x)) + 1)
        #plt.xticks(x_list)

        plt.plot(x, self.white_wins_list, label=self.white_player)
        plt.plot(x, self.black_wins_list, label=self.black_player)
        plt.xlabel("Rounds")
        plt.ylabel("Wins")
        self.white_player_name = self.white_player
        self.black_player_name = self.black_player
        match self.white_player:
            case "MCTS-MR" | "MCTS-MB":
                self.white_player_name = self.white_player + " Depth:" + str(self.white_Depth)
            case "MCTS-MS":
                self.white_player_name = self.white_player + " Depth:" + str(self.white_Depth) + " Threshold:" + str(self.white_Threshold)
        match self.black_player:
            case "MCTS-MR" | "MCTS-MB":
                self.black_player_name = self.black_player + " Depth:" + str(self.black_Depth)
            case "MCTS-MS":
                self.black_player_name = self.black_player + " Depth:" + str(self.black_Depth) + " Threshold:" + str(self.black_Threshold)

        plt.title(f"{self.white_player_name} vs {self.black_player_name}, Time {self.time}, Iterations {self.iterations}")
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
