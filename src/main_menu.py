import pygame as pg
import pygame_gui as pg_gui
from pygame_gui.elements import UIButton, UILabel

from constants import SIZE, WIDTH, HEIGHT
from constants import BLACK
from single_player import single_player
from deepq_mode import train

clock = pg.time.Clock()
manager = pg_gui.UIManager(SIZE, '../res/theme.json')

# drawing menu
sp_button = UIButton(relative_rect=pg.Rect((WIDTH//2-WIDTH//10, HEIGHT//2-HEIGHT//40), (WIDTH//5, HEIGHT//20)),
                     text='Single Player',
                     manager=manager)
dqm_button = UIButton(relative_rect=pg.Rect((WIDTH//2-WIDTH//10, HEIGHT//2+HEIGHT//40), (WIDTH//5, HEIGHT//20)),
                      text='AI Mode',
                      manager=manager)
title_text = UILabel(relative_rect=pg.Rect((WIDTH//2-WIDTH//4, HEIGHT//3), (WIDTH//2, HEIGHT//10)),
                     text='Snake with Self-Learning AI',
                     manager=manager)


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

            manager.process_events(event)

        win.fill(BLACK)

        manager.update(time_delta)

        manager.draw_ui(win)

        pg.display.update()
