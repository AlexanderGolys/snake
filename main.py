from pygame.locals import *
import pygame
import random
import copy
import sys
import time

SQUARELENGHT = 20
SQUARENB = 40

FPS = 30
BGCOLOR = (40, 40, 40)
WHITE = (255, 255, 255)
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4


def main(best):
    FIRSTPOS = [20, 20]
    pygame.init()
    global FPSCLOCK, DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((SQUARELENGHT*SQUARENB, SQUARELENGHT*SQUARENB))
    pygame.display.set_caption("Snake")
    pygame.key.set_repeat(200, 1)
    snake = [FIRSTPOS]
    apple = rand_apple(snake)
    feed = False
    while True:
        best = max(best, len(snake))
        if if_game_over(snake):
            while True:
                draw_game_over(DISPLAYSURF)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                time.sleep(1)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        main(best)

        else:
            draw(DISPLAYSURF, snake, apple, best)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    snake = move(snake, UP, feed)
                    feed = False
                if event.key == K_DOWN:
                    snake = move(snake, DOWN, feed)
                    feed = False
                if event.key == K_RIGHT:
                    snake = move(snake, RIGHT, feed)
                    feed = False
                if event.key == K_LEFT:
                    snake = move(snake, LEFT, feed)
                    feed = False

        if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
            feed = True
            apple = rand_apple(snake)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def draw_game_over(surface):
    surface.fill(BGCOLOR)
    game_over_img = pygame.image.load('./graphics/over.png')
    surface.blit(game_over_img, (200, 300))


def draw(surface, snake, apple, best):
    surface.fill(BGCOLOR)
    snake_img = pygame.image.load('./graphics/snake.png')
    apple_img = pygame.image.load('./graphics/apple.png')
    head_img = pygame.image.load('./graphics/head.png')
    surface.blit(apple_img, (apple[0]*SQUARELENGHT, apple[1]*SQUARELENGHT))
    surface.blit(head_img, (snake[0][0] * SQUARELENGHT, snake[0][1] * SQUARELENGHT))

    for pos in snake[1:]:
        surface.blit(snake_img, (pos[0]*SQUARELENGHT, pos[1]*SQUARELENGHT))

    font_obj = pygame.font.Font('freesansbold.ttf', 15)
    score_surface = font_obj.render('score:  ' + str(len(snake)), True, WHITE, BGCOLOR)
    score_rect = score_surface.get_rect()
    score_rect.center = (700, 700)
    surface.blit(score_surface, score_rect)

    font_obj = pygame.font.Font('freesansbold.ttf', 15)
    best_surface = font_obj.render('best:  ' + str(best), True, WHITE, BGCOLOR)
    best_rect = best_surface.get_rect()
    best_rect.center = (700, 720)
    surface.blit(best_surface, best_rect)


def move(snake, where, feed):
    last = snake[-1].copy()
    old_snake = copy.deepcopy(snake)

    if where == UP:
        snake[0][1] -= 1
    elif where == RIGHT:
        snake[0][0] += 1
    elif where == DOWN:
        snake[0][1] += 1
    else:
        snake[0][0] -= 1


    for nb in range(len(snake)):
        if nb > 0:
            snake[nb] = old_snake[nb - 1]

    if feed:
        snake.append(last)
    return snake


def rand_apple(snake):
    x = random.randint(0, SQUARENB-1)
    y = random.randint(0, SQUARENB-1)
    for pos in snake:
        if pos[0] == x and pos[1] == y:
            return rand_apple(snake)
    return x, y


def if_game_over(snake):
    if eat_himself(snake):
        return True
    return not (0 <= snake[0][0] < SQUARENB and 0 <= snake[0][1] < SQUARENB)


def eat_himself(x):
    _size = len(x)
    repeated = []
    for i in range(_size):
        k = i + 1
        for j in range(k, _size):
            if x[i][0] == x[j][0] and x[i][1] == x[j][1] and x[i] not in repeated:
                repeated.append(x[i])
    return not repeated == []




main(1)
