import random
import pygame as pg

from constants import *


class Food:
    def __init__(self):
        self.spawn()

    # randomly choose position for food
    def spawn(self):
        self.x, self.y = random.randrange(
            BLOCKS_X) * GRID_DIV, random.randrange(BLOCKS_Y) * GRID_DIV

    # draw food onto window
    def draw(self, win):
        pg.draw.rect(
            win, RED, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    # check if the snake has eaten the food
    def check_eaten(self, snake):
        head = snake.head_pos()
        if head[0] == self.x and head[1] == self.y:
            self.spawn()

            while (self.x, self.y) in snake.positions:
                self.spawn()

            snake.positions.insert(0, (head[0], head[1]))

            snake.score += 1
