import tkinter as tk
from PIL import Image, ImageTk
from Game import LionBoard


class LionGUI:
    def __init__(self, frame):
        self.frame = frame
        self.canvas = tk.Canvas(self.frame, width=1000, height=700)
        self.canvas.pack()

        self.base_x = 314
        self.base_y = 102
        self.images = []
        self.animals = [None] * 12
        self.captures = [None] * 6
        """self.white_captures_1 = [None]
        self.white_captures_2 = [None]
        self.white_captures_3 = [None]
        self.black_captures_1 = [None]
        self.black_captures_2 = [None]
        self.black_captures_3 = [None]"""
        self.board = LionBoard.LionBoard()
        self.whiteTurn = True

        # Draw Background
        img = Image.open("../GUI_Resources/Catch_The_Lion_Board.png")
        resized_image = img.resize((1000, 700))
        self.images.append(ImageTk.PhotoImage(resized_image))
        self.canvas.create_image(500, 350, image=self.images[-1])

        #Load Animal Images
        """img = Image.open("../GUI_Resources/Hen.jpg")
        resized_image = img.resize((121, 121))
        self.Hen = resized_image
        self.animals_img.append(resized_image)
        x = 0 % 3
        y = 3 - int(0 / 3)
        self.canvas.create_image(self.base_x + x * 126 + 58, self.base_y + y * 126 + 58, image=self.animals_img[-1])"""

        """img = Image.open("../GUI_Resources/Hen.jpg")
        resized_image = img.resize((121, 121))
        self.Hen = resized_image
        self.animals_img.append(resized_image)"""

        """img = Image.open("../GUI_Resources/Chicken.jpg")
        resized_image = img.resize((121, 121))
        self.Chicken = resized_image
        img = Image.open("../GUI_Resources/Lion.jpg")
        resized_image = img.resize((121, 121))
        self.Lion = resized_image
        img = Image.open("../GUI_Resources/Giraffe.jpg")
        resized_image = img.resize((121, 121))
        self.Giraffe = resized_image
        img = Image.open("../GUI_Resources/Elephant.jpg")
        resized_image = img.resize((121, 121))
        self.Elephant = resized_image

        img = Image.open("../GUI_Resources/Black_Hen.jpeg")
        resized_image = img.resize((121, 121))
        self.Black_Hen = resized_image
        img = Image.open("../GUI_Resources/Black_Lion.jpeg")
        resized_image = img.resize((121, 121))
        self.Black_Lion = resized_image
        img = Image.open("../GUI_Resources/Black_Chicken.jpeg")
        resized_image = img.resize((121, 121))
        self.Black_Chicken = resized_image
        img = Image.open("../GUI_Resources/Black_Elephant.jpeg")
        resized_image = img.resize((121, 121))
        self.Black_Elephant = resized_image
        img = Image.open("../GUI_Resources/Black_Giraffe.jpeg")
        resized_image = img.resize((121, 121))
        self.Black_Giraffe = resized_image

        img = Image.open("../GUI_Resources/Hen.jpg")
        resized_image = img.resize((121, 121))
        self.images.append(ImageTk.PhotoImage(resized_image))
        x = 0 % 3
        y = 3 - int(0 / 3)
        self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])"""

    def create_rectangle(self, x, y, a, b, **options):
        if 'alpha' in options:
            # Calculate the alpha transparency for every color(RGB)
            alpha = int(options.pop('alpha') * 255)
            # Use the fill variable to fill the shape with transparent color
            fill = options.pop('fill')
            fill = root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (a - x, b - y), fill)
            self.images.append(ImageTk.PhotoImage(image))
            image = self.canvas.create_image(x, y, image=self.images[-1], anchor='nw')
            rectangle = self.canvas.create_rectangle(x, y, a, b, **options)
            return rectangle, image

    def draw_animal(self, index: int, animal:str):
        if self.animals[index]:
            self.canvas.delete(self.animals[index])
        x = index % 3
        y = 3 - int(index / 3)
        match animal:
            case "L":
                self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Lion.jpg").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "H":
                self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Hen.jpg").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "C":
                self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Chicken.jpg").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "G":
                self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Giraffe.jpg").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "E":
                self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Elephant.jpg").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "l":
                self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Lion.jpeg").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "g":
                self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Giraffe.jpeg").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "e":
                self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Elephant.jpeg").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "c":
                self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Chicken.jpeg").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])
            case "h":
                self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Hen.jpeg").resize((121, 121))))
                self.animals[index] = self.canvas.create_image(self.base_x + x * 126 + 59, self.base_y + y * 126 + 59, image=self.images[-1])

    def delete_animal(self, index: int):
        if self.animals[index]:
            self.canvas.delete(self.animals[index])

    def draw_reserve(self, animal: str):
        match animal:
            case 'E':
                if not self.captures[0]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Elephant.jpeg").resize((75, 75))))
                    self.captures[0] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 0 * 126 + 36, image=self.images[-1])
            case 'G':
                if not self.captures[1]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Giraffe.jpeg").resize((75, 75))))
                    self.captures[1] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 1 * 80 + 36,image=self.images[-1])
            case 'C':
                if not self.captures[2]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Chicken.jpeg").resize((75, 75))))
                    self.captures[2] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 2 * 80 + 36,image=self.images[-1])
            case 'e':
                if not self.captures[3]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Elephant.jpg").resize((75, 75))))
                    self.captures[3] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 5 * 80 + 59, image=self.images[-1])
            case 'g':
                if not self.captures[4]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Giraffe.jpg").resize((75, 75))))
                    self.captures[4] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 4 * 80 + 59, image=self.images[-1])
            case 'c':
                if not self.captures[5]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Chicken.jpg").resize((75, 75))))
                    self.captures[5] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 3 * 80 + 59, image=self.images[-1])

    """case 'E':
                if not self.black_captures_1[0]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Elephant.jpeg").resize((75, 75))))
                    self.black_captures_1[0] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 0 * 126 + 36, image=self.images[-1])
            case 'G':
                if not self.black_captures_2[0]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Giraffe.jpeg").resize((75, 75))))
                    self.black_captures_2[0] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 1 * 80 + 36, image=self.images[-1])
            case 'C':
                if not self.black_captures_3[0]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Black_Chicken.jpeg").resize((75, 75))))
                    self.black_captures_3[0] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 2 * 80 + 36, image=self.images[-1])
            case 'e':
                if not self.white_captures_1[0]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Elephant.jpg").resize((75, 75))))
                    self.white_captures_1[0] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 5 * 80 + 59, image=self.images[-1])
            case 'g':
                if not self.white_captures_2[0]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Giraffe.jpg").resize((75, 75))))
                    self.white_captures_2[0] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 4 * 80 + 59, image=self.images[-1])
            case 'c':
                if not self.white_captures_3[0]:
                    self.images.append(ImageTk.PhotoImage(Image.open("../GUI_Resources/Chicken.jpg").resize((75, 75))))
                    self.white_captures_3[0] = self.canvas.create_image(self.base_x - 126 + 55, self.base_y + 3 * 80 + 59, image=self.images[-1])"""

    def draw_board_fen(self, Fen:str):
        self.board.setBoard_Fen(Fen)
        self.whiteTurn = True
        #self.white_captures = []
        #self.black_captures = []
        i = 11
        for char in Fen:
            if char.isdigit():
                i = i - int(char)
            elif i < 0:
                # captures
                self.draw_reserve(char)
            elif char == '/':
                continue
            else:
                #print(f"Index:{i} Animal:{char}")
                self.draw_animal(i, char)
                i = i - 1

    def clear_board(self):
        for fig in self.animals:
            if fig:
                self.canvas.delete(fig)

        for fig in self.captures:
            if fig:
                self.canvas.delete(fig)

    def draw_board(self):
        self.clear_board()
        self.draw_board_fen(self.board.getFen())

    def makeMove(self, x:int, y:int):
        if self.board.makeMove(self.whiteTurn, x, y):
            self.delete_animal(y)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")

    Lion_frame = tk.Frame(root)
    GUI = LionGUI(Lion_frame)
    Lion_frame.pack(expand=True, fill="both")
    Lion_frame.tkraise()

    #GUI.create_rectangle(310 + 5, 100 + 3, 435 - 3, 225 - 5, fill="blue", alpha=.3)
    #GUI.draw_animal(0, "L")
    GUI.draw_board_fen("elg/1c1/1C1/GLE/")
    GUI.board.randomBoard()
    #GUI.clear_board()
    print(GUI.board.getFen())
    #GUI.draw_board_fen(GUI.board.getFen())
    GUI.draw_board()
    #GUI.draw_board()
    #GUI.draw_reserve("E")
    #GUI.draw_reserve("G")
    #GUI.draw_reserve("C")
    #GUI.draw_reserve("e")
    #GUI.draw_reserve("g")
    #GUI.draw_reserve("c")
    #GUI.draw_animal(0, "L")
    root.mainloop()
