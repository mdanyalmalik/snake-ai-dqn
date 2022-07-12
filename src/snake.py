import pygame as pg
from pygame.constants import K_a, K_d, K_s, K_w
from food import Food

from constants import *


class Snake:
    def __init__(self, x, y):
        self.vx, self.vy = V, 0
        self.positions = [(x, y), (x-GRID_DIV, y),
                          (x-2*GRID_DIV, y)]
        self.score = 0
        self.food = Food()

    def head_pos(self):
        return self.positions[0]

    def move(self):
        keys = pg.key.get_pressed()
        if keys[K_w] and not self.vy == V:
            self.vx, self.vy = 0, -V
        elif keys[K_a] and not self.vx == V:
            self.vx, self.vy = -V, 0
        elif keys[K_s] and not self.vy == -V:
            self.vx, self.vy = 0, V
        elif keys[K_d] and not self.vx == -V:
            self.vx, self.vy = V, 0

        head = self.head_pos()

        new_x = head[0] + self.vx
        new_y = head[1] + self.vy

        self.positions.insert(0, (new_x, new_y))
        self.positions.pop()

    def check_collision(self):
        head = self.head_pos()

        if head in self.positions[2:]:
            self.reset()

        if head[0] >= WIDTH or head[0] < 0 or head[1] >= HEIGHT or head[1] < 0:
            self.reset()

    def draw(self, win):
        for pos in self.positions:
            pg.draw.rect(win, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

    def draw_score(self, win, font):
        self.score_render = font.render(f'Score: {self.score} ', False, WHITE)
        self.text_width = self.score_render.get_rect().width
        win.blit(self.score_render, (WIDTH-self.text_width, 0))

    def food_draw(self, win):
        self.food.draw(win=win)

    def food_check_eaten(self):
        self.food.check_eaten(self)

    def reset(self):
        self.vx, self.vy = V, 0
        x, y = (WIDTH//2, HEIGHT//2)
        self.positions = [(x, y), (x-GRID_DIV, y),
                          (x-2*GRID_DIV, y)]
        self.score = 0
        self.food.spawn()
