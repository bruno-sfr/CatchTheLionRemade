import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path

# import requi9red module
#import sys

# append the path of the
# parent directory
#sys.path.append("..")

from Game import LionBoard, Move
from AlphaBeta import IterativeDeepening, AlphaBeta
from MonteCarlo import MCTS_Solvers


class LionGUI:
    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        self.canvas = tk.Canvas(self.frame, width=1000, height=700)
        self.mouse_func = None
        self.canvas.pack()
        self.firstclick = True
        self._from = 0
        self._to = 0
        self.AI_time = 0

        self.base_x = 314
        self.base_y = 102
        self.images = []
        self.markers = [None] * 12
        self.markers_img = [None] * 12
        self.animals = [None] * 12
        self.captures = [None] * 6

        self.board = LionBoard.LionBoard()
        self.whiteTurn = True
        self.AB = IterativeDeepening.iterativeDeepeningAB()
        self.MTD = IterativeDeepening.iterativeDeepeningMTD()

        # Draw Background
        #Path(f"../GUI_Resources").mkdir(parents=True, exist_ok=True)
        img = Image.open("../GUI_Resources/Catch_The_Lion_Board.png")
        resized_image = img.resize((1000, 700))
        self.images.append(ImageTk.PhotoImage(resized_image))
        self.canvas.create_image(500, 350, image=self.images[-1])
        self.Animal_color = "Color"

        self.GameText = self.canvas.create_text(500, 50, text="Catch the Lion", fill="black", font=('Helvetica 20 bold'))
        self.PvP_button = tk.Button(self.canvas, text="Player vs Player", command=self.PvP_View, anchor="center")
        self.PvA_button = tk.Button(self.canvas, text="Player vs AI", command=self.PvA_View, anchor="center")
        options = ["Color", "Black_White"]
        self.Color_select = ttk.Combobox(self.frame, values=options)
        self.Color_select.set("Select Color of Animals")  # Set a default selection
        self.Color_select.bind("<<ComboboxSelected>>", self.on_color_select)


        self.window_1 = self.canvas.create_window(850, 110, width=170, height=30, window=self.PvP_button)
        self.window_2 = self.canvas.create_window(850, 150, width=170, height=30, window=self.PvA_button)
        self.window_3 = self.canvas.create_window(850, 180, width=170, height=30)
        self.window_4 = self.canvas.create_window(850, 220, width=170, height=30)
        self.window_5 = self.canvas.create_window(850, 260, width=170, height=30)
        self.canvas.itemconfig(self.window_3, window=self.Color_select)
        self.canvas.itemconfig(self.window_3, state="normal")
        self.canvas.itemconfig(self.window_4, state="hidden")
        self.canvas.itemconfig(self.window_5, state="hidden")

    def quitGame(self, event):
        self.root.destroy()

    def begin_game(self):
        self.clear_board()
        self.draw_board_fen("elg/1c1/1C1/GLE/")
        #self.draw_board_fen("3/2L/2l/3/")
        self.mouse_func = self.canvas.bind("<Button-1>", self.on_mouse_click_game)
        self.whiteTurn = True
        self.update_game_text(self.whiteTurn)

    def begin_game_AI(self):
        self.AI_time = int(self.time_entry.get())
        self.clear_board()
        self.draw_board_fen("elg/1c1/1C1/GLE/")
        self.mouse_func = self.canvas.bind("<Button-1>", self.on_mouse_click_game_AI)
        self.whiteTurn = True
        self.update_game_text(self.whiteTurn)

    def default_view(self):
        self.clear_board()
        self.PvP_button = tk.Button(self.canvas, text="Player vs Player", command=self.PvP_View, anchor="center")
        self.PvA_button = tk.Button(self.canvas, text="Player vs AI", command=self.PvA_View, anchor="center")
        options = ["Color", "Black_White"]
        self.Color_select = ttk.Combobox(self.frame, values=options)
        self.Color_select.set("Select Color of Animals")  # Set a default selection
        self.Color_select.bind("<<ComboboxSelected>>", self.on_color_select)

        self.canvas.itemconfig(self.window_1, window=self.PvP_button)
        self.canvas.itemconfig(self.window_2, window=self.PvA_button)
        self.canvas.itemconfig(self.window_3, window=self.Color_select)
        self.canvas.itemconfig(self.window_3, state="normal")
        self.canvas.itemconfig(self.window_4, state="hidden")
        self.canvas.itemconfig(self.window_5, state="hidden")

    def PvP_View(self):
        self.Begin_button = tk.Button(self.canvas, text="Begin Game", command=self.begin_game, anchor="center")
        self.Go_back_button = tk.Button(self.canvas, text="Go Back", command=self.default_view, anchor="center")
        self.canvas.itemconfig(self.window_1, window=self.Begin_button)
        self.canvas.itemconfig(self.window_2, window=self.Go_back_button)
        self.canvas.itemconfig(self.window_3, state="hidden")
        #self.canvas.itemconfig(self.button1, text="Begin Game", command=self.begin_game)
        #self.canvas.itemconfig(self.button2, text="Go Back Game", command=self.begin_game)

    def PvA_View(self):
        self.Begin_button = tk.Button(self.canvas, text="Begin AI Game", command=self.begin_game_AI, anchor="center")
        self.Go_back_button = tk.Button(self.canvas, text="Go Back", command=self.default_view, anchor="center")
        self.time_label = tk.Label(self.canvas, text="Time per turn:")
        self.time_entry = tk.Entry(self.frame)

        options = ["Alpha-Beta", "Alpha-Beta with TT", "MTD(f)", "MCTS-Solver", "MCTS-MR", "MCTS-MS", "MCTS-MB"]

        self.AI_select = ttk.Combobox(self.frame, values=options)
        self.AI_select.set("Select AI Player")  # Set a default selection
        self.AI_select.bind("<<ComboboxSelected>>", self.on_AI_select)

        self.canvas.itemconfig(self.window_1, window=self.AI_select)
        self.canvas.itemconfig(self.window_2, window=self.time_label)
        self.canvas.itemconfig(self.window_3, window=self.time_entry)
        self.canvas.itemconfig(self.window_4, window=self.Begin_button)
        self.canvas.itemconfig(self.window_5, window=self.Go_back_button)
        self.canvas.itemconfig(self.window_3, state="normal")
        self.canvas.itemconfig(self.window_4, state="normal")
        self.canvas.itemconfig(self.window_5, state="normal")

    def on_AI_select(self, event):
        selected_item = self.AI_select.get()
        self.AI_player = selected_item

    def on_color_select(self, event):
        selected_item = self.Color_select.get()
        self.Animal_color = selected_item

    def end_game(self):
        if self.board.hasWhiteWon():
            self.canvas.itemconfig(self.GameText, text="White has won!")
        elif self.board.hasBlackWon():
            self.canvas.itemconfig(self.GameText, text="Black has won!")
        else:
            raise Exception("In end Game even tho no one has won")
        self.canvas.unbind("<Button 1>", self.mouse_func)


    def create_rectangle(self, x, y, a, b, **options):
        if 'alpha' in options:
            # Calculate the alpha transparency for every color(RGB)
            alpha = int(options.pop('alpha') * 255)
            # Use the fill variable to fill the shape with transparent color
            fill = options.pop('fill')
            fill = self.root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (a - x, b - y), fill)
            self.images.append(ImageTk.PhotoImage(image))
            image = self.canvas.create_image(x, y, image=self.images[-1], anchor='nw')
            rectangle = self.canvas.create_rectangle(x, y, a, b, **options)
            return rectangle, image

    def update_game_text(self, whiteTurn:bool):
        if whiteTurn:
            self.canvas.itemconfig(self.GameText, text="White´s Turn")
        else:
            self.canvas.itemconfig(self.GameText, text="Black´s Turn")

    def on_mouse_click_game_AI(self, event):
        x, y = event.x, event.y
        try:
            index = self.get_index(x, y)
        except Exception:
            return
        if self.firstclick:
            self._from = index
            list = self.board.allpossibleMoves_BigList(self.whiteTurn)
            for move in list:
                if move.getFrom() == self._from:
                    self.mark_field(move.getTo())
            self.firstclick = not self.firstclick
        else:
            self.clear_marks()
            if self.whiteTurn:
                if index == "c" or index == "g" or index == "e" or self.board.white.isSquareSet(index):
                    self._from = index
                    list = self.board.allpossibleMoves_BigList(self.whiteTurn)
                    for move in list:
                        if move.getFrom() == self._from:
                            self.mark_field(move.getTo())
                    return
            else:
                if index == "c" or index == "g" or index == "e" or self.board.black.isSquareSet(index):
                    self._from = index
                    list = self.board.allpossibleMoves_BigList(self.whiteTurn)
                    for move in list:
                        if move.getFrom() == self._from:
                            self.mark_field(move.getTo())
                    return

            self._to = index
            if not(self.makeMove(self._from, self._to)):
                return
            print("eval:",self.board.eval_func())
            if not (self.board.isGameOver()):
                self.canvas.itemconfig(self.GameText, text="AI´s Turn")
                self.canvas.update()
                self.make_AI_Move()
                self.firstclick = not self.firstclick

    def on_mouse_click_game(self, event):
        x, y = event.x, event.y
        try:
            index = self.get_index(x, y)
        except Exception:
            return
        if self.firstclick:
            self._from = index
            list = self.board.allpossibleMoves_BigList(self.whiteTurn)
            for move in list:
                if move.getFrom() == self._from:
                    self.mark_field(move.getTo())
            self.firstclick = not self.firstclick
        else:
            self.clear_marks()
            if self.whiteTurn:
                if index == "c" or index == "g" or index == "e" or self.board.white.isSquareSet(index):
                    self._from = index
                    list = self.board.allpossibleMoves_BigList(self.whiteTurn)
                    for move in list:
                        if move.getFrom() == self._from:
                            self.mark_field(move.getTo())
                    return
            else:
                if index == "c" or index == "g" or index == "e" or self.board.black.isSquareSet(index):
                    self._from = index
                    list = self.board.allpossibleMoves_BigList(self.whiteTurn)
                    for move in list:
                        if move.getFrom() == self._from:
                            self.mark_field(move.getTo())
                    return

            self._to = index
            self.makeMove(self._from, self._to)
            self.firstclick = not self.firstclick

        #print(f"Animal: {animal} Index: {index}")

    def mark_field(self, index:int):
        x = index % 3
        y = 3 - int(index / 3)
        rect, img = self.create_rectangle(self.base_x + x * 126, self.base_y + y * 126, self.base_x + x * 126 + 2*59, self.base_y + y * 126 + 2*59, fill="blue", alpha=.3)
        self.markers.append(rect)
        self.markers_img.append(img)

    def clear_marks(self):
        for i in self.markers:
            self.canvas.delete(i)
        for i in self.markers_img:
            self.canvas.delete(i)

    def get_index(self, x:int, y:int):
        #animal = True
        index = 0
        if self.base_x + 59 - 60 < x < self.base_x + 59 + 2 * 126 + 60 and self.base_y + 59 - 60 < y < self.base_y + 59 + 3 * 126 + 60:
            #animal = True
            index_x = (x-(self.base_x+59))/126
            index_x = round(index_x)
            index_y = (y - (self.base_y + 59)) / 126
            index_y = round(index_y)
            index = abs(3 - index_y) * 3 + index_x
        elif self.base_x - 126 + 55 - 32 < x < self.base_x - 126 + 55 + 32 and self.base_y + 0 * 80 + 36 - 32 < y < self.base_y + 5 * 80 + 59 + 32:
            #animal = False
            if y < self.base_y + 2 * 80 + 36 + 32:
                index = (y-(self.base_y+36))/80
            elif y > self.base_y + 3 * 80 + 59 - 32:
                index = (y - (self.base_y + 59)) / 80
            else:
                raise Exception("Input out of Grid Bounds")
            index = round(index)
            match index:
                case 0:
                    index = 'e'
                case 1:
                    index = 'g'
                case 2:
                    index = 'c'
                case 3:
                    index = 'c'
                case 4:
                    index = 'g'
                case 5:
                    index = 'e'
        else:
            raise Exception("Input out of Grid Bounds")
        return index

    def draw_animal(self, index: int, animal:str):
        if self.animals[index]:
            self.canvas.delete(self.animals[index])
        x = index % 3
        y = 3 - int(index / 3)
        match animal:
            case "L":
                self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Lion.png").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "H":
                self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Hen.png").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "C":
                self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Chicken.png").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "G":
                self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Giraffe.png").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "E":
                self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Elephant.png").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "l":
                self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Black_Lion.png").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "g":
                self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Black_Giraffe.png").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "e":
                self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Black_Elephant.png").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "c":
                self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Black_Chicken.png").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "h":
                self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Black_Hen.png").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])

    def delete_animal(self, index: int):
        if self.animals[index]:
            self.canvas.delete(self.animals[index])

    def draw_reserve(self, animal: str):
        match animal:
            case 'e':
                if not self.captures[0]:
                    self.images.append(ImageTk.PhotoImage(Image.open(
                        f"../GUI_Resources/{self.Animal_color}/Black_Elephant.png").resize((75, 75))))
                    self.captures[0] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 0 * 80 + 36, image=self.images[-1])
            case 'g':
                if not self.captures[1]:
                    self.images.append(ImageTk.PhotoImage(Image.open(
                        f"../GUI_Resources/{self.Animal_color}/Black_Giraffe.png").resize((75, 75))))
                    self.captures[1] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 1 * 80 + 36,image=self.images[-1])
            case 'c':
                if not self.captures[2]:
                    self.images.append(ImageTk.PhotoImage(Image.open(
                        f"../GUI_Resources/{self.Animal_color}/Black_Chicken.png").resize((75, 75))))
                    self.captures[2] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 2 * 80 + 36,image=self.images[-1])
            case 'E':
                if not self.captures[3]:
                    self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Elephant.png").resize((75, 75))))
                    self.captures[3] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 5 * 80 + 59, image=self.images[-1])
            case 'G':
                if not self.captures[4]:
                    self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Giraffe.png").resize((75, 75))))
                    self.captures[4] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 4 * 80 + 59, image=self.images[-1])
            case 'C':
                if not self.captures[5]:
                    self.images.append(ImageTk.PhotoImage(Image.open(f"../GUI_Resources/{self.Animal_color}/Chicken.png").resize((75, 75))))
                    self.captures[5] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 3 * 80 + 59, image=self.images[-1])

    def delete_reserve(self, index:int):
        if self.captures[index]:
            self.canvas.delete(self.captures[index])

    def draw_board_fen(self, Fen:str):
        self.board.setBoard_Fen(Fen)
        i = 11
        for char in Fen:
            if char.isdigit():
                i = i - int(char)
            elif char == '/':
                continue
            elif i < 0:
                # captures
                self.draw_reserve(char)
            else:
                self.draw_animal(i, char)
                i = i - 1

    def clear_board(self):
        for i in range(len(self.animals)):
            if self.animals[i]:
                self.canvas.delete(self.animals[i])
                self.animals[i] = None

        for i in range(len(self.captures)):
            if self.captures[i]:
                self.canvas.delete(self.captures[i])
                self.captures[i] = None

    def draw_board(self):
        self.clear_board()
        self.draw_board_fen(self.board.getFen())

    def make_AI_Move(self):
        print("AI whiteturn:", self.whiteTurn)
        match self.AI_player:
            case "Alpha-Beta":
                eval, move, depth = self.AB.iterativeDeepening_AB(self.AI_time, self.board, self.whiteTurn)
                self.makeMove(move.getFrom(), move.getTo())
            case "Alpha-Beta with TT":
                eval, move, depth = self.AB.iterativeDeepening_AB_TT(self.AI_time, self.board, self.whiteTurn)
                self.makeMove(move.getFrom(), move.getTo())
            case "MTD(f)":
                 eval, move, depth = self.MTD.iterativeDeepening_MTD(self.AI_time, self.board, self.whiteTurn)
                 self.makeMove(move.getFrom(), move.getTo())
            case "MCTS-Solver":
                result_node = MCTS_Solvers.MCTS_Solver_Run(self.board, self.whiteTurn, self.AI_time)
                self.makeMove(result_node.move.getFrom(), result_node.move.getTo())
            case "MCTS-MR":
                result_node = MCTS_Solvers.MCTS_MR_Run(self.board, self.whiteTurn, self.AI_time, 1)
                self.makeMove(result_node.move.getFrom(), result_node.move.getTo())
            case "MCTS-MS":
                result_node = MCTS_Solvers.MCTS_MS_Run(self.board, self.whiteTurn, self.AI_time, 2, 4)
                self.makeMove(result_node.move.getFrom(), result_node.move.getTo())
            case "MCTS-MB":
                result_node = MCTS_Solvers.MCTS_MB_Run(self.board, self.whiteTurn, self.AI_time, 3)
                self.makeMove(result_node.move.getFrom(), result_node.move.getTo())

    def makeMove(self, x:int, y:int):
        if self.board.makeMove(self.whiteTurn, x, y):
            self.draw_board()
            if self.board.isGameOver():
                self.end_game()
                return True
            self.whiteTurn = not self.whiteTurn
            self.update_game_text(self.whiteTurn)
            return True
        return False