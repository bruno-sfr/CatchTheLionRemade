from GUI import LionBoard_GUI, Simulator_GUI
import tkinter as tk
from PIL import Image, ImageTk


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x700")
        self.root.title("Catch the Lion!")
        self.frame = tk.Frame(self.root)
        self.current_frame = self.frame
        self.images = []
        self.canvas = tk.Canvas(self.frame, width=1000, height=700)
        self.canvas.pack()

        self.game_frame = tk.Frame(self.root)
        self.game = LionBoard_GUI.LionGUI(self.root, self.game_frame)
        self.sim_frame = tk.Frame(self.root)
        self.sim = Simulator_GUI.SimGUI(self.root, self.sim_frame)

        self.Game_button = tk.Button(self.canvas, text="Game", command=lambda: self.show_frame(self.game_frame), anchor="center")
        self.Sim_button = tk.Button(self.canvas, text="Simulation", command=lambda: self.show_frame(self.sim_frame), anchor="center")

        self.window_1 = self.canvas.create_window(500, 300, width=200, height=30, window=self.Game_button)
        self.window_2 = self.canvas.create_window(500, 350, width=200, height=30, window=self.Sim_button)

        # Draw Background
        img = Image.open("../GUI_Resources/Catch_The_Lion_Simple.png")
        resized_image = img.resize((1000, 700))
        self.images.append(ImageTk.PhotoImage(resized_image))
        self.canvas.create_image(500, 350, image=self.images[-1])

    def show_frame(self, frame):
        try:
            self.current_frame.pack_forget()
        except NameError:
            pass
        frame.pack(expand=True, fill="both")
        frame.tkraise()
        self.current_frame = frame

    def Start_GUI(self):
        self.show_frame(self.frame)
        self.root.mainloop()


if __name__ == "__main__":
    GUI = GUI()
    GUI.Start_GUI()
