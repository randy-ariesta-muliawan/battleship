import tkinter as tk
import sys
import time

from config import Config
from game_stat import Statistic
from ship import Ship
from player import Player
from board import Board
from PIL import Image, ImageTk

class Window(tk.Tk):

	def __init__(self, Game):
		self.game = Game # Battleship - my_battleship
		self.config = Game.config

		super().__init__()
		self.title(self.config.title)
		self.geometry(self.config.screen)

		self.create_container()

		self.pages = {}
		self.create_board()
		self.create_play()


	def create_container(self):
		self.container = tk.Frame(self, bg="white")
		self.container.pack(fill="both", expand=True)

	def create_board(self):
		self.pages["board"] = Board(self.container, self.game)

	def create_play(self):
		self.pages['Play'] = Play(self.container, self)

	def change_page(self):
		board = self.pages["board"]
		board.tkraise()


class Play(tk.Frame):

	def __init__(self, parent, App):
		self.application = App
		self.settings = App.config

		super().__init__(parent)
		self.configure(bg="blue")
		# self.pack(fill="both", expand=True)
		self.grid(row=0, column=0, sticky="nsew")
		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.mainFrame = tk.Frame(self, bg="blue")
		self.mainFrame.pack(expand=True)

		image = Image.open(self.settings.logo_path)
		image_w, image_h = image.size # (tuple)


		image = image.resize((int(image_w//3), int(image_h//3)))
		self.logo = ImageTk.PhotoImage(image)
		self.label_logo = tk.Label(self.mainFrame, image=self.logo)
		self.label_logo.pack()
		self.play_btn = tk.Button(self.mainFrame, text="PLAY", font=("Arial", 14, "bold"), command=lambda:self.application.change_page())
		self.play_btn.pack(pady=5)


class Battleship:

	def __init__(self):
		self.config = Config()
		self.ship = Ship(self)
		self.player = Player()
		self.window = Window(self)

	def check_location(self):
		if self.ship.location == self.player.location:
			return True
		return False

	def is_button_clicked(self, pos_x, pos_y):
		print(f"{pos_x, pos_y}")
		self.player.current_location(pos_x, pos_y)
		win = self.check_location()
		self.window.pages["board"].change_photo_button(pos_x, pos_y, win)
		if win:
			print("YOU WIN!")
			time.sleep(2)
			sys.exit() # self.window.destroy()

	def run(self):
		self.window.mainloop()


def main():
	my_battleship = Battleship()
	my_battleship.run()

if __name__ == '__main__':
	main()