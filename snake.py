import pygame as pg
from pygame.constants import K_a, K_d, K_s, K_w
from food import Food

from constants import width, height, grid_div, v, block_size
from constants import black, white, green, red


class Snake:
    def __init__(self, x, y):
        self.vx, self.vy = v, 0
        self.positions = [(x, y), (x-grid_div, y),
                          (x-2*grid_div, y)]
        self.score = 0
        self.food = Food()

    def head_pos(self):
        return self.positions[0]

    def move(self):
        keys = pg.key.get_pressed()
        if keys[K_w] and not self.vy == v:
            self.vx, self.vy = 0, -v
        elif keys[K_a] and not self.vx == v:
            self.vx, self.vy = -v, 0
        elif keys[K_s] and not self.vy == -v:
            self.vx, self.vy = 0, v
        elif keys[K_d] and not self.vx == -v:
            self.vx, self.vy = v, 0

        head = self.head_pos()

        new_x = head[0] + self.vx
        new_y = head[1] + self.vy

        self.positions.insert(0, (new_x, new_y))
        self.positions.pop()

    def check_collision(self):
        head = self.head_pos()

        if head in self.positions[2:]:
            self.reset()

        if head[0] >= width or head[0] < 0 or head[1] >= height or head[1] < 0:
            self.reset()

    def draw(self, win):
        for pos in self.positions:
            pg.draw.rect(win, green, (pos[0], pos[1], block_size, block_size))

    def draw_score(self, win, font):
        self.score_render = font.render(str(self.score), False, white)
        win.blit(self.score_render, (width-60, 0))

    def food_draw(self, win):
        self.food.draw(win=win)

    def food_check_eaten(self):
        self.food.check_eaten(self)

    def reset(self):
        self.vx, self.vy = v, 0
        x, y = (width//2, height//2)
        self.positions = [(x, y), (x-grid_div, y),
                          (x-2*grid_div, y)]
        self.score = 0
        self.food.spawn()
