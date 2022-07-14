import pygame as pg
import pygame_gui as pg_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton

from constants import *
from single_player import single_player
from deepq_mode import train

clock = pg.time.Clock()
myfont = pg.font.Font('../res/Exo-Light.ttf', WIDTH//20)
manager = UIManager(SIZE, '../res/theme.json')

# drawing menu
sp_button = UIButton(relative_rect=pg.Rect((WIDTH//2-WIDTH//10, HEIGHT//2-HEIGHT//40), (WIDTH//5, HEIGHT//20)),
                     text='Single Player',
                     manager=manager)
dqm_button = UIButton(relative_rect=pg.Rect((WIDTH//2-WIDTH//10, HEIGHT//2+HEIGHT//40), (WIDTH//5, HEIGHT//20)),
                      text='AI Mode',
                      manager=manager)
info_button = UIButton(relative_rect=pg.Rect((WIDTH//2-WIDTH//10, HEIGHT//2+3*HEIGHT//40), (WIDTH//5, HEIGHT//20)),
                       text='Info',
                       manager=manager)
close_button = UIButton(relative_rect=pg.Rect((WIDTH-WIDTH//10, HEIGHT-HEIGHT//20), (WIDTH//10, HEIGHT//20)),
                        text='Quit',
                        manager=manager)


def draw_title(win, font):
    title_render = font.render('Snake with Self-learning AI', False, WHITE)
    text_width = title_render.get_rect().width
    win.blit(title_render, (WIDTH//2-text_width//2, HEIGHT//2-HEIGHT//5))


def main_menu(win):
    run = True

    while run:
        time_delta = clock.tick(60)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                quit()
            elif event.type == pg_gui.UI_BUTTON_PRESSED:
                if event.ui_element == sp_button:
                    single_player(win)
                elif event.ui_element == dqm_button:
                    train(win)
                elif event.ui_element == info_button:
                    pass
                elif event.ui_element == close_button:
                    run = False
                    quit()

            manager.process_events(event)

        win.fill(BLACK)

        manager.update(time_delta)

        manager.draw_ui(win)
        draw_title(win=win, font=myfont)

        pg.display.update()
