import pygame as pg

from constants import SIZE
from main_menu import main_menu

if __name__ == '__main__':
    pg.init()

    win = pg.display.set_mode(SIZE)
    pg.display.set_caption('Snake')

    icon = pg.image.load('snake.png')
    pg.display.set_icon(icon)

    main_menu(win)
