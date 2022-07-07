import pygame as pg
from pygame.constants import K_ESCAPE

from snake import Snake
from constants import WIDTH, HEIGHT
from constants import BLACK

snake1 = Snake(WIDTH//2, HEIGHT//2)

pg.init()
pg.font.init()
clock = pg.time.Clock()
myfont = pg.font.SysFont('Times New Roman', 30)


def single_player(win):
    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False

        win.fill(BLACK)

        snake1.draw(win=win)
        snake1.move()
        snake1.draw_score(win=win, font=myfont)
        snake1.food_check_eaten()
        snake1.food_draw(win=win)
        snake1.check_collision()

        clock.tick(24)
        pg.display.update()
