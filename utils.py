import pygame, sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from pygame.font import Font
import settings as s
import random

def try_quit(e):
    if e.type == QUIT or\
      (e.type == KEYDOWN and\
       e.key == K_ESCAPE):
        pygame.quit()
        sys.exit()
