import pygame as pg
import pygame_gui as pg_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton

from constants import *

clock = pg.time.Clock()
myfont = pg.font.Font('../res/Exo-Light.ttf', WIDTH//50)

manager = UIManager(SIZE, '../res/theme.json')
back_button = UIButton(relative_rect=pg.Rect((0, 0), (WIDTH//10, HEIGHT//20)),
                       text='Back',
                       manager=manager)

ABOUT = "A snake clone with deep Q learning AI."


def draw_text(text, pos, win, font):
    text_render = font.render(text, False, WHITE)
    text_width = text_render.get_rect().width
    win.blit(text_render, (pos[0]-text_width//2, pos[1]))


def info_page(win):
    run = True

    while run:
        time_delta = clock.tick(60)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                quit()
            elif event.type == pg_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    run = False

            manager.process_events(event)

        win.fill(BLACK)

        manager.update(time_delta)

        manager.draw_ui(win)
        draw_text(text=ABOUT, pos=(WIDTH//2, HEIGHT//2), win=win, font=myfont)

        pg.display.update()
