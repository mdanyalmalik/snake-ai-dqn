import pygame as pg
import pygame_gui as pg_gui
from pygame.constants import K_ESCAPE
from pygame_gui import UIManager
from pygame_gui.elements import UIButton

from snake import Snake
from constants import *

snake1 = Snake(WIDTH//2, HEIGHT//2)

pg.init()
pg.font.init()
clock = pg.time.Clock()
myfont = pg.font.Font('../res/Exo-Light.ttf', WIDTH//40)

# setting up UI manager from pygame gui and adding button
manager = UIManager(SIZE, '../res/theme.json')
back_button = UIButton(relative_rect=pg.Rect((0, 0), (WIDTH//10, HEIGHT//20)),
                       text='Back',
                       manager=manager)


def single_player(win):  # main loop
    run = True

    while run:
        time_delta = clock.tick(24)/1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
            elif event.type == pg_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    run = False

            manager.process_events(event)

        win.fill(BACKGROUND)

        snake1.draw(win=win)
        snake1.move()
        snake1.draw_score(win=win, font=myfont)
        snake1.food_check_eaten()
        snake1.food_draw(win=win)
        snake1.check_collision()

        manager.update(time_delta)
        manager.draw_ui(win)

        pg.display.update()
