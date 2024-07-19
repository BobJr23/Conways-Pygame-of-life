import pygame
import numpy as np

import time
pygame.init()
WIDTH = 800
HEIGHT = WIDTH + 100
# dimensions of the grid, maybe make it dynamic later?
GRID_COORD = 50
box_size = WIDTH / GRID_COORD
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 40)

pygame.display.set_caption("GAME OF LIFE!")
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (104, 173, 66)
TEMPLATE = np.zeros((GRID_COORD, GRID_COORD))
grid = np.copy(TEMPLATE)
pause = True
run = True
clock = pygame.time.Clock()
timer = 0


def set_value(game, row, column, val):
    game[row, column] = val
    return game


def check_tile(game, row, column):
    if row < 0 or row > (GRID_COORD - 1) or column < 0 or column > (GRID_COORD - 1):
        return 0
    ret = game[row, column]

    return ret


def check_all_neighbors(game, row, column):
    total = 0
    # Checks all neighbors, returns 0 if not found
    total += check_tile(game, row, column + 1)
    total += check_tile(game, row, column - 1)
    total += check_tile(game, row + 1, column)
    total += check_tile(game, row - 1, column)
    total += check_tile(game, row - 1, column - 1)
    total += check_tile(game, row + 1, column + 1)
    total += check_tile(game, row + 1, column - 1)
    total += check_tile(game, row - 1, column + 1)
    return total

while run:
    clock.tick(FPS)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # UPDATE BOX
