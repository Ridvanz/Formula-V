import pygame, sys
from pygame.locals import *
from pygame.font import Font
import settings as s
import random


def generate_obstacle_coords(seed=0):
    
    random.seed(seed)
    obstacles_y = [0]
    for i in range(s.NUM_OBSTACLES):
        randint = random.randint(100,200)
        obstacles_y.append(obstacles_y[i] + randint)

    obstacles_y = [x/obstacles_y[-1]*(s.TRACK_LENGTH-s.SPAWN_AREA)+s.SPAWN_AREA for x in obstacles_y][:-1]
    obstacles_x = [random.randint(0.5*s.ENEMY_SIZE[0], s.WINDOW_WIDTH - 1.5*s.ENEMY_SIZE[0]) for x in range(len(obstacles_y))]

    return obstacles_x, obstacles_y


def try_quit(e):
    if e.type == QUIT or\
      (e.type == pygame.KEYDOWN and\
       e.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()

def limit(v, low, high):
    """Returns v, limited to low/high threshold"""
    if v < low:
        return low
    elif v > high:
        return high
    else:
        return v

def render_text(text, window, font, color, position):
    """Renders a font and blits it to the given window"""
    text = font.render(text, 1, color)

    window.blit(text, position)

    return text


def __game_over_overlay(window):
    font_size
    go_font = pygame.font.Font(pygame.font.get_default_font(), 44)
    txt_go  = go_font.render("Game Over", 1, s.COLOURS["red"])
    x       = (s.DIMENSIONS[0] - txt_go.get_size()[0]) / 2
    y       = (s.DIMENSIONS[1] - txt_go.get_size()[1]) / 2
    overlay = pygame.Surface(s.DIMENSIONS, pygame.SRCALPHA)

    overlay.fill((255, 255, 255, 90))
    overlay.blit(txt_go, (x, y))
    window.blit(overlay, (0,0))