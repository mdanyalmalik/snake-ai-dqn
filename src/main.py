import pygame as pg

from constants import *
from main_menu import main_menu

if __name__ == '__main__':
    pg.init()  # initialise pygame for the whole program

    win = pg.display.set_mode(SIZE)
    pg.display.set_caption('Snake')

    icon = pg.image.load('../res/snake.png')
    pg.display.set_icon(icon)

    main_menu(win)  # launch main menu, the rest of the logic handled there
