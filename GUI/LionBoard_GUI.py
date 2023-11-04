import tkinter as tk
from PIL import Image, ImageTk


class LionGUI:
    def __init__(self, frame):
        self.frame = frame

        self.canvas = tk.Canvas(self.frame, width=1000, height=700)
        self.canvas.pack()
        self.images = []
        self.animals = [None] * 12
        self.base_x = 314
        self.base_y = 102

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

    def draw_board_fen(self, Fen:str):
        self.white_captures = []
        self.black_captures = []
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
            elif char == '/':
                continue
            else:
                #print(f"Index:{i} Animal:{char}")
                self.draw_animal(i, char)
                i = i - 1

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
    #GUI.draw_animal(0, "L")
    root.mainloop()
