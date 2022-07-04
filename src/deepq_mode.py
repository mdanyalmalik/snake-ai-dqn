from collections import deque
import os
import numpy as np
import random
import torch
import pygame as pg
from pygame.constants import K_ESCAPE, K_UP, K_DOWN

from dqsnake import DQSnake
from constants import BLOCK_SIZE, V, WIDTH, HEIGHT
from constants import BLACK
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

pg.init()
pg.font.init()
myfont = pg.font.SysFont('Times New Roman', 15)

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(12, 512, 4)
        self.model = self.model.to(device)
        self.loaded = False

        # load model if it is saved
        model_file_path = '../models'
        models = os.listdir(model_file_path)
        if models:
            self.model.load_state_dict(torch.load(
                os.path.join(model_file_path, models[0]), map_location=device)['state_dict'])
            self.loaded = True

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
        if not self.loaded:
            self.epsilon = 80 - self.n_games

        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float).to(device)
            prediction = self.model(state0)
            move = torch.argmax(prediction)
            final_move[move] = 1

        return final_move


def train(win):
    record = 0

    agent = Agent()
    snake = DQSnake(WIDTH//2, HEIGHT//2)

    delay = 0
    delay_inc = 1

    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                quit()

        keys = pg.key.get_pressed()
        if keys[K_ESCAPE]:
            run = False
        elif keys[K_UP]:
            delay += delay_inc
        elif keys[K_DOWN]:
            if delay > 0:
                delay -= delay_inc

        win.fill(BLACK)

        state_old = agent.get_state(snake)

        final_move = agent.get_action(state_old)

        snake.move(final_move)
        snake.frame_iteration += 1

        reward = 0
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
                agent.model.save(
                    score=score, optimiser=agent.trainer.optimiser)

        snake.draw(win=win)
        snake.draw_info(win=win, font=myfont,
                        game_no=agent.n_games, record=record, delay=delay)
        snake.food_draw(win=win)

        pg.time.delay(delay)
        pg.display.update()
