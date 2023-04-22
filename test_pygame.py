# coding=latin-1

import pygame
from pygame.locals import *
from pygame.rect import *

from tkinter import messagebox

import numpy as np

import sys

from fights.envs import quoridor
from minimax_agent import MinimaxAgent

sys.path.append("../")

# 1. ���� �ʱ�ȭ
pygame.init()

# 2. ����â �ɼ� ����
board_size = 700
tile_ratio = 0.8
wall_ratio = 0.2
player_ratio = 0.5
tile_width = board_size * tile_ratio / 9
wall_width = board_size * wall_ratio / 8
total_width = tile_width + wall_width
player_width = board_size * player_ratio / 9

size = [board_size, board_size]
screen = pygame.display.set_mode(size)

# 3. ���� �� �ʿ��� ����

clock = pygame.time.Clock()

tiles = [[Rect(j*total_width,
               i*total_width,
               tile_width,
               tile_width) for i in range(9)] for j in range(9)]
horizontal_wall = [[Rect(j*total_width,
                       i*total_width+tile_width,
                       tile_width,
                       wall_width) for i in range(8)] for j in range(9)]
vertical_wall = [[Rect(j*total_width+tile_width,
                         i*total_width,
                         wall_width,
                         tile_width) for i in range(9)] for j in range(8)]
center_poll = [[Rect(j*total_width+tile_width,
                     i*total_width+tile_width,
                     wall_width,
                     wall_width) for i in range(8)] for j in range(8)]
player = [Rect(0, 0, player_width, player_width), Rect(0, 0, player_width, player_width)]

# red : 0, orange : 1, yellow : 2, green : 3, blue: 4, purple : 5, white : 6, black : 7

black = (0, 0, 0)
white = (255, 255, 255)
grey = (150, 150, 150)
red = (255, 59, 47)
orange = (255, 133, 47)
yellow = (255, 214, 62)
green = (1, 137, 101)
blue = (77, 156, 222)
purple = (176, 90, 177)
leaf = (146, 208, 80)
sky = (139, 190, 233)


def clear():
    ...


def aabb(a, b):
    return a.left < b[0] < a.left + a.width and a.top < b[1] < a.top + a.height


def msg_over():
    messagebox.showinfo('warning!', 'It\'s over!')


def msg_warning1():
    messagebox.showwarning('warning!', 'You can not move it there')


def msg_warning2():
    messagebox.showwarning('warning!', 'You can not put a wall there')


def msg_warning3():
    messagebox.showwarning('warning!', 'You can not rotate there')


# 4. ���� �̺�Ʈ
SB = 0

state_memory = []
state = quoridor.QuoridorEnv().initialize_state()

agents = [MinimaxAgent(0, 0), MinimaxAgent(1, 0)]
whose_turn = 0
mouse_clicked = False

while SB == 0:

    # 4-1. FPS ����
    clock.tick(60)

    # 4-2. ���� �Է� ����
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if not state.done:
                    state_memory.append(state)
                    state = quoridor.QuoridorEnv().step(state, whose_turn, agents[whose_turn](state))
                    if state.done:
                        msg_over()
                    whose_turn = 1 - whose_turn
                else:
                    msg_over()
            elif event.key == pygame.K_p:
                state = state_memory[-1]
                state_memory.pop(-1)
                whose_turn = 1 - whose_turn
        if pygame.mouse.get_pressed()[0]:
            if not mouse_clicked:
                mouse_clicked = True
                mospos = pygame.mouse.get_pos()
                for i in range(9):
                    for j in range(9):
                        if aabb(tiles[i][j], mospos):
                            action = [0, i, j]
                            try:
                                next_state = quoridor.QuoridorEnv().step(state, whose_turn, action)
                            except:
                                ...
                            else:
                                state_memory.append(state)
                                state = next_state
                                whose_turn = 1 - whose_turn
                                if state.done:
                                    msg_over()
                for i in range(8):
                    for j in range(8):
                        if aabb(horizontal_wall[i][j], mospos):
                            action = [1, i, j]
                            try:
                                next_state = quoridor.QuoridorEnv().step(state, whose_turn, action)
                            except:
                                ...
                            else:
                                state_memory.append(state)
                                state = next_state
                                whose_turn = 1 - whose_turn
                                if state.done:
                                    msg_over()
                for i in range(8):
                    for j in range(8):
                        if aabb(vertical_wall[i][j], mospos):
                            action = [2, i, j]
                            try:
                                next_state = quoridor.QuoridorEnv().step(state, whose_turn, action)
                            except:
                                ...
                            else:
                                state_memory.append(state)
                                state = next_state
                                whose_turn = 1 - whose_turn
                                if state.done:
                                    msg_over()
        else:
            mouse_clicked = False

    # 4-3. �Է�, �ð��� ���� ��ȭ

    # 4-4. �׸���
    screen.fill(grey)

    title = "Red's remaining walls : " + str(state.walls_remaining[0]) + " // Blue's remaining walls : " + str(state.walls_remaining[1])
    pygame.display.set_caption(title)       

    for i in range(9):
        for j in range(9):
            pygame.draw.rect(screen, white, tiles[i][j])
    for i in range(9):
        for j in range(8):
            if state.board[2][i][j]:
                pygame.draw.rect(screen, black, horizontal_wall[i][j])
            if state.board[3][j][i]:
                pygame.draw.rect(screen, black, vertical_wall[j][i])

    mospos = pygame.mouse.get_pos()
    for i in range(9):
        for j in range(9):
            if aabb(tiles[i][j], mospos):
                try:
                    next_state = quoridor.QuoridorEnv().step(state, whose_turn, (0, i, j))
                except:
                    ...
                else:
                    pygame.draw.rect(screen, purple, tiles[i][j])
    for i in range(8):
        for j in range(8):
            if aabb(horizontal_wall[i][j], mospos):
                try:
                    next_state = quoridor.QuoridorEnv().step(state, whose_turn, (1, i, j))
                except:
                    ...
                else:
                    pygame.draw.rect(screen, purple, horizontal_wall[i][j])
                    pygame.draw.rect(screen, purple, horizontal_wall[i+1][j])
                    pygame.draw.rect(screen, purple, center_poll[i][j])
    for i in range(8):
        for j in range(8):
            if aabb(vertical_wall[i][j], mospos):
                try:
                    next_state = quoridor.QuoridorEnv().step(state, whose_turn, (2, i, j))
                except:
                    ...
                else:
                    pygame.draw.rect(screen, purple, vertical_wall[i][j])
                    pygame.draw.rect(screen, purple, vertical_wall[i][j+1])
                    pygame.draw.rect(screen, purple, center_poll[i][j])

    agent0_pos = np.argwhere(state.board[0])[0]
    agent1_pos = np.argwhere(state.board[1])[0]
    player[0].left = agent0_pos[0] * total_width + tile_width / 2 - player[0].width / 2
    player[0].top = agent0_pos[1] * total_width + tile_width / 2 - player[0].height / 2
    player[1].left = agent1_pos[0] * total_width + tile_width / 2 - player[0].width / 2
    player[1].top = agent1_pos[1] * total_width + tile_width / 2 - player[0].height / 2

    pygame.draw.rect(screen, red, player[0])
    pygame.draw.rect(screen, blue, player[1])

    # 4-5. ������Ʈ

    pygame.display.flip()

# 5. ���� ����
pygame.quit()
