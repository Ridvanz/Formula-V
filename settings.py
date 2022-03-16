from pygame import Color
import math, os

FPS                   = 60
SCREEN_WIDTH          = 1200
SCREEN_HEIGHT         = 800
WINDOW_WIDTH          = 400
WINDOW_HEIGHT         = 800
TITLE_SCREEN          = True
RENDER                = True
SOUND                 = True
VOLUME                = 0.7

TRACK_LENGTH          = 1e5


SPAWN_AREA            = 1000
NUM_OBSTACLES         = 500
HORIZON               = 1000
ENEMY_SIZE            = (40, 40)
PLAYER_SIZE           = (40, 60)

WHITE                 = (255, 255, 255)
BLACK                 = (0, 0, 0)
RED                   = (255, 0, 0)
GREEN                 = (0, 255, 0)
BLUE                  = (0, 0, 255)
YELLOW                = (255, 255, 255)

# FONTS                 = {"retro_computer": os.path.join("lib", "PressStart2P.ttf"),
#                          "fipps": os.path.join("lib", "Fipps-Regular.otf")}
COLOURS               = {"white": Color(255, 255, 255),
                         "opaque_white": Color(255, 255, 255, 80),
                         "text": Color(172, 199, 252),
                         "dark_text": Color(57, 84, 137),
                         "selection": [Color(172, 199, 252),Color(100, 149, 252)],
                         "sky": Color(10, 10, 10),
                         "gutter": Color(100, 100, 100),
                         "red": Color(204, 0, 0),
                         "green": Color(0, 204, 0),
                         "black": Color(0, 0, 0),}

