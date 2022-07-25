import pygame as pg
import pygame_gui as pg_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIButton

from constants import *

clock = pg.time.Clock()  # pygame clock object
myfont = pg.font.Font('../res/Exo-Light.ttf', WIDTH//50)  # font of choice

# setting up and adding components to manager object from pygame gui
manager = UIManager(SIZE, '../res/theme.json')
back_button = UIButton(relative_rect=pg.Rect((0, 0), (WIDTH//10, HEIGHT//20)),
                       text='Back',
                       manager=manager)

# text to display
ABOUT = 'A snake clone with a self-learning AI mode, where the agent makes use of reinforcement learning to teach itself the game. This is done via the use of a deep Q learning model written using pytorch. Furthermore, there is also a single-player mode to see how well you can do compared to the AI.'


# custom function to draw text on multiple lines using pygame
def draw_text(text, pos, win, font):
    CH_PER_LINE = 50  # (maximum) characters per line

    line, start, stop = 0, 0, 0

    while stop != len(text):
        start = stop
        if len(text[start:]) >= CH_PER_LINE:
            stop += CH_PER_LINE
            while text[stop] != ' ':
                stop -= 1
        else:
            stop += len(text[start:])

        text_render = font.render(text[start:stop], False, WHITE)
        text_width = text_render.get_rect().width
        text_height = text_render.get_rect().height
        win.blit(text_render, (pos[0]-text_width//2, pos[1]+line*text_height))

        line += 1


def info_page(win):  # main loop
    run = True

    while run:
        time_delta = clock.tick(60)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                quit()
            elif event.type == pg_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    run = False

            manager.process_events(event)

        win.fill(BACKGROUND)

        manager.update(time_delta)

        manager.draw_ui(win)
        draw_text(text=ABOUT, pos=(WIDTH//2, HEIGHT//3), win=win, font=myfont)

        pg.display.update()
