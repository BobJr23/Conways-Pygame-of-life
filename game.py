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


def update_grid(g):
    t = time.time()
    copy = np.copy(g)
    for index, value in np.ndenumerate(g):
        neighbor_count = check_all_neighbors(g, *index)
        if (value == 1 and neighbor_count == 2) or neighbor_count == 3:
            copy[index] = 1
        else:
            copy[index] = 0

    draw_image(copy)
    print(time.time()-t)
    return copy


def draw_image(g):
    WIN.fill(BLACK)
    # draw boxes
    for ind, v in np.ndenumerate(np.copy(g)):
        if v == 1:
            pygame.draw.rect(WIN, GREEN, (*[i * box_size for i in ind], box_size, box_size))
        else:
            pygame.draw.rect(WIN, BLACK, (*[i * box_size for i in ind], box_size, box_size))
    for it in range(GRID_COORD):
        pygame.draw.line(WIN, WHITE, (box_size * it, 0), (box_size * it, WIDTH), 2)
        pygame.draw.line(WIN, WHITE, (0, box_size * it), (WIDTH, box_size * it), 2)


draw_image(grid)
while run:
    clock.tick(FPS)
    timer += 1
    if timer % 15 == 0 and not pause:
        grid = update_grid(grid)

    pause_button = pygame.draw.rect(WIN, WHITE, (WIDTH / 2 - 100, WIDTH, 200, 80))
    WIN.blit(
        FONT.render(
            "Start/Stop",
            False,
            GREEN,
        ),
        (WIDTH / 2 - 70, WIDTH + 30),
    )

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            location = pygame.mouse.get_pos()
            if pause_button.collidepoint(location):
                if pause:
                    pause = False
                else:
                    pause = True
            elif location[1] <= 800:
                tile = [int(i / box_size) for i in location]
                if grid[tile[0], tile[1]] == 1:
                    grid[tile[0], tile[1]] = 0
                else:
                    grid[tile[0], tile[1]] = 1
                draw_image(grid)
    # UPDATE BOX
