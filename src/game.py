import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, KEYDOWN, K_ESCAPE, K_w, K_a, K_s, K_d
# import sys
import src.settings as s
# import numpy as np
from src.simulate import set_seed, game_update, get_initial_state, size, N
# import numpy as np

class Game:
    """Provides game flow."""

    def __init__(self, seed=None, render_mode = False):

        if seed is not None:
            set_seed(seed)

        self.render_mode = render_mode
        self.reset()
        self.stopped = False
    
    def reset(self):
        self.player, self.obstacles, self.idx, self.observation = get_initial_state()
        self.ticks = 0
        self.finished = False
        self.render_initialized = False
    
    def update(self, action):
        
        self.u_x, self.u_y = action
        
        if self.render_mode:
            self.u_x, self.u_y = self._get_control_input(action)

        self.player, self.obstacles, self.idx, self.observation = game_update(
            (self.u_x, self.u_y), self.player, self.obstacles, self.idx
        )

        # if self.player[1] > s.TRACK_LENGTH:
        #     self.finished = True

        if self.ticks > s.GAME_LENGTH:
            self.finished = True
        
        self.ticks += 1

        # if s.DEBUG:
        #     print(f"fps: {self.clock.get_fps()}")

    def observe(self):

        # passed = int(self.obstacles[self.idx, 1] < -size)

        # obstacles = self.obstacles[[(self.idx + i + passed) % N for i in range(4)], :]
        # observation = {"player": self.player, "obstacles": obstacles, "ticks": self.ticks}
        
        return self.observation

    def render(self):
        
        if not self.render_initialized:
            self._init_render()
            
        red = max(0, min(255, self.player[3] * 5 * 255))
        self.window.fill((red, 255, 255 - red))

        color = (0, 0, 0)
        player_surf = pygame.Surface(self.size)
        player_surf.fill(color)

        player_x = self.player[0] * (s.WINDOW_WIDTH - self.size[0])
        player_y = s.WINDOW_HEIGHT - 2 * self.size[1]

        self.window.blit(player_surf, (player_x, player_y))

        color = (255, 0, 0)
        obstacle_surf = pygame.Surface(self.size)
        obstacle_surf.fill(color)

        for i in range(self.obstacles.shape[0]):
            if self.obstacles[i, 3]:
                obstacle_x = self.obstacles[i, 0] * (s.WINDOW_WIDTH - self.size[0])
                obstacle_y = (1 - self.obstacles[i, 1]) * (
                    s.WINDOW_WIDTH
                ) - 2 * self.size[1]

                self.window.blit(obstacle_surf, (obstacle_x, obstacle_y))

        text_color = (255, 0, 255)
        self.display.fill(s.BLACK)
        self.display.blit(
            self.window,
            (
                (s.SCREEN_WIDTH - s.WINDOW_WIDTH) / 2,
                (s.SCREEN_HEIGHT - s.WINDOW_HEIGHT) / 2,
            ),
        )

        font = pygame.font.SysFont("Arial", 16)
        fps = font.render(f"FPS: {round(self.clock.get_fps(),2)}", True, text_color)
        speed = font.render(f"Speed: {round(self.player[3],2)}", True, text_color)
        ticks = font.render(f"Ticks: {self.ticks}", True, text_color)
        distance_left = font.render(
            f"Distance traveled: {round(self.player[1], 2)}",
            True,
            text_color,
        )

        text_x = s.WINDOW_WIDTH + (s.SCREEN_WIDTH - s.WINDOW_WIDTH) / 2 + 5

        self.display.blit(fps, (text_x, 20))
        self.display.blit(speed, (text_x, 60))
        self.display.blit(ticks, (text_x, 100))
        self.display.blit(distance_left, (text_x, 140))

        pygame.display.update()

        # for e in pygame.event.get():

        #     if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
        #         pygame.quit()
        #         sys.exit()
        
        self.clock.tick(s.FPS)


    def _get_control_input(self, action):

        if not self.render_initialized:
            self._init_render()

        (u_x, u_y) = action

        pressed_keys = pygame.key.get_pressed()
        if any(pressed_keys):

            u_x = u_y = 0

            if pressed_keys[K_UP] or pressed_keys[K_w]:
                u_y += 1
                # move_up_sound.play()
            if pressed_keys[K_DOWN] or pressed_keys[K_s]:
                u_y -= 1
                # move_down_sound.play()

            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                u_x += 1
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                u_x -= 1
                
            if pressed_keys[K_ESCAPE]:
                self.stop()

        pygame.event.clear()

        return u_x, u_y

    def _init_render(self):
        self.display = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        pygame.display.set_caption("Formula V")
        self.clock = pygame.time.Clock()

        pygame.init()
        # pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.event.set_blocked(None)
        pygame.event.set_allowed(KEYDOWN)

        self.window = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT))
        self.size = (size * s.WINDOW_WIDTH, size * s.WINDOW_HEIGHT)

        if s.SOUND:
            pygame.mixer.init()
            pygame.mixer.music.load("assets/music/game.mp3")
            pygame.mixer.music.play(loops=-1)

        self.render_initialized = True

    def stop(self):
        
        # if s.SOUND:
        #     pygame.mixer.music.stop()
        #     pygame.mixer.quit()
                    
        if self.render_mode:
            pygame.display.quit()
            pygame.quit()

        self.stopped = True
