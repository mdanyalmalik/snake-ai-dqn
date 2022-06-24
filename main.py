import pygame as pg
from pygame.constants import K_a, K_d, K_s, K_w, K_ESCAPE
import pygame_gui as pg_gui

from snake import Snake
from constants import width, height, grid_div, size
from constants import black, white, green, red

pg.init()

pg.font.init()
myfont = pg.font.SysFont('Comic Sans MS', 30)

win = pg.display.set_mode(size)
pg.display.set_caption('Snake')

manager = pg_gui.UIManager(size, 'theme.json')

icon = pg.image.load('snake.png')
pg.display.set_icon(icon)

clock = pg.time.Clock()


def draw_grid():
    for line in range(width//grid_div+1):
        pg.draw.line(win, white, (line*grid_div, 0), (line*grid_div, height))
    for line in range(height//grid_div+1):
        pg.draw.line(win, white, (0, line*grid_div), (width, line*grid_div))


snake1 = Snake(width//2, height//2)

# drawing menu
sp_button = pg_gui.elements.UIButton(relative_rect=pg.Rect((width//2-width//10, height//2-height//40), (width//5, height//20)),
                                     text='Single Player',
                                     manager=manager)
title_text = pg_gui.elements.UILabel(relative_rect=pg.Rect((width//2-width//4, height//3), (width//2, height//10)),
                                     text='Snake with Self-Learning AI',
                                     manager=manager)


def menu():
    run = True

    while run:
        time_delta = clock.tick(60)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                quit()
            elif event.type == pg_gui.UI_BUTTON_PRESSED:
                if event.ui_element == sp_button:
                    single_player()

            manager.process_events(event)

        win.fill(black)

        manager.update(time_delta)

        manager.draw_ui(win)

        pg.display.update()


def single_player():
    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                quit()

        keys = pg.key.get_pressed()
        if keys[K_ESCAPE]:
            run = False

        win.fill(black)
        draw_grid()

        snake1.draw(win=win)
        snake1.move()
        snake1.draw_score(win=win, font=myfont)
        snake1.food_check_eaten()
        snake1.food_draw(win=win)
        snake1.check_collision()

        pg.time.delay(50)
        pg.display.update()


menu()
