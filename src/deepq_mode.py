from collections import deque
import numpy as np
import random
from sklearn.metrics import SCORERS
import torch
import pygame as pg
from pygame.constants import K_ESCAPE

from dqsnake import DQSnake
from constants import SIZE, BLOCK_SIZE, V, WIDTH, HEIGHT
from constants import BLACK
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

pg.init()
pg.font.init()
myfont = pg.font.SysFont('Times New Roman', 30)


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(12, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, snake):
        head = snake.head_pos()

        point_u = (head[0], head[1]-BLOCK_SIZE)
        point_d = (head[0], head[1]+BLOCK_SIZE)
        point_l = (head[0]-BLOCK_SIZE, head[1])
        point_r = (head[0]+BLOCK_SIZE, head[1])

        direction = [
            snake.vy == -V,
            snake.vy == V,
            snake.vx == -V,
            snake.vx == V
        ]

        food_direction = [
            snake.food.y < head[1],
            snake.food.y > head[1],
            snake.food.x < head[0],
            snake.food.x > head[0],
        ]

        state = [
            snake.check_collision(point_u)[1],
            snake.check_collision(point_d)[1],
            snake.check_collision(point_l)[1],
            snake.check_collision(point_r)[1],

            direction[0],
            direction[1],
            direction[2],
            direction[3],

            food_direction[0],
            food_direction[1],
            food_direction[2],
            food_direction[3],
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards,
                                next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        self.epsilon = 200 - self.n_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction)
            final_move[move] = 1


def train(win):
    total_score = 0
    record = 0

    agent = Agent()
    snake = DQSnake(WIDTH//2, HEIGHT//2)

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

        state_old = agent.get_state(snake)

        final_move = agent.get_action(state_old)

        final_move = [0, 0, 0, 0]
        final_move[random.randint(0, 3)] = 1

        reward = 0
        snake.move(final_move)
        r1, game_over = snake.check_collision()
        r2 = snake.food_check_eaten()

        reward = reward + r1 + r2

        state_new = agent.get_state(snake)

        agent.train_short_memory(
            state_old, final_move, reward, state_new, game_over)

        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            score = snake.score
            snake.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score',
                  score, 'Record', record)
            total_score += score

        snake.draw(win=win)
        snake.draw_score(win=win, font=myfont)
        snake.food_draw(win=win)

        # pg.time.delay(15)
        pg.display.update()


win = pg.display.set_mode(SIZE)

if __name__ == '__main__':
    train(win)
