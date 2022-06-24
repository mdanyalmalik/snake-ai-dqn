import random
import pygame as pg

from constants import grid_div, block_size, blocks
from constants import black, white, green, red


class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.x, self.y = random.randrange(
            blocks) * grid_div, random.randrange(blocks) * grid_div

    def draw(self, win):
        pg.draw.rect(
            win, red, (self.x, self.y, block_size, block_size))

    def check_eaten(self, snake):
        head = snake.head_pos()
        if head[0] == self.x and head[1] == self.y:
            self.spawn()

            while (self.x, self.y) in snake.positions:
                self.spawn()

            snake.positions.insert(0, (head[0], head[1]))

            snake.score += 1
