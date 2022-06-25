import random
import pygame as pg

from constants import GRID_DIV, BLOCK_SIZE, BLOCKS
from constants import RED


class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.x, self.y = random.randrange(
            BLOCKS) * GRID_DIV, random.randrange(BLOCKS) * GRID_DIV

    def draw(self, win):
        pg.draw.rect(
            win, RED, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    def check_eaten(self, snake):
        head = snake.head_pos()
        if head[0] == self.x and head[1] == self.y:
            self.spawn()

            while (self.x, self.y) in snake.positions:
                self.spawn()

            snake.positions.insert(0, (head[0], head[1]))

            snake.score += 1
