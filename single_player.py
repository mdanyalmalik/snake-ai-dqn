import pygame as pg
from pygame.constants import K_a, K_d, K_s, K_w, K_ESCAPE

from snake import Snake
from constants import WIDTH, HEIGHT
from constants import BLACK

snake1 = Snake(WIDTH//2, HEIGHT//2)

pg.init()
pg.font.init()
myfont = pg.font.SysFont('Times New Roman', 30)


def single_player(win):
    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                quit()

        keys = pg.key.get_pressed()
        if keys[K_ESCAPE]:
            run = False

        win.fill(BLACK)

        snake1.draw(win=win)
        snake1.move()
        snake1.draw_score(win=win, font=myfont)
        snake1.food_check_eaten()
        snake1.food_draw(win=win)
        snake1.check_collision()

        pg.time.delay(50)
        pg.display.update()
