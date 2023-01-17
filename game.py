import pygame
import settings as s
import numpy as np
from simulate import game_update, get_initial_state, size, N

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, KEYDOWN, K_ESCAPE


class Game:
    """Provides game flow."""

    def __init__(self, seed):

        # self.seed            = seed
        np.random.seed(seed)

        self.player, self.obstacles, self.idx = get_initial_state()
        self.ticks = 0
        self.finished = False

        if s.RENDER:

            self.display = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
            pygame.display.set_caption("Formula V")
            self.clock = pygame.time.Clock()

            pygame.init()
            pygame.event.set_blocked(pygame.MOUSEMOTION)

            self.window = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT))
            self.size = (size * s.WINDOW_WIDTH, size * s.WINDOW_HEIGHT)

            if s.SOUND:
                pygame.mixer.init()
                pygame.mixer.music.load("assets/music/game.mp3")
                pygame.mixer.music.play(loops=-1)

    def update(self, action):

        if s.RENDER:
            u_x, u_y = self._get_control_input(action)

        self.player, self.obstacles, self.idx = game_update(
            (u_x, u_y), self.player, self.obstacles, self.idx
        )

        if self.player[1] > s.TRACK_LENGTH:
            self.finished = True

        self.ticks += 1

        if s.DEBUG:
            print(f"fps: {self.clock.get_fps()}")

    def observe(self):

        passed = int(self.obstacles[self.idx, 1] < -size)

        obstacles = self.obstacles[[(self.idx + i + passed) % N for i in range(4)], :]
        states = {"player": self.player, "obstacles": obstacles}

        print((self.idx + 0 + passed) % N)

        return states

    def _get_control_input(self, action):

        (u_x, u_y) = action

        pressed_keys = pygame.key.get_pressed()
        if any(pressed_keys):

            u_x = u_y = 0

            if pressed_keys[K_UP]:
                u_y += 1
                # move_up_sound.play()
            if pressed_keys[K_DOWN]:
                u_y -= 1
                # move_down_sound.play()

            if pressed_keys[K_RIGHT]:
                u_x += 1
            if pressed_keys[K_LEFT]:
                u_x -= 1

        return u_x, u_y

    def render(self):
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
            f"Distance left: {round(s.TRACK_LENGTH-self.player[1], 2)}",
            True,
            text_color,
        )

        text_x = s.WINDOW_WIDTH + (s.SCREEN_WIDTH - s.WINDOW_WIDTH) / 2 + 5

        self.display.blit(fps, (text_x, 20))
        self.display.blit(speed, (text_x, 60))
        self.display.blit(ticks, (text_x, 100))
        self.display.blit(distance_left, (text_x, 140))

        pygame.display.update()

        for e in pygame.event.get():

            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        self.clock.tick(s.FPS)

    def _stop(self):
        if s.SOUND:
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        if s.RENDER:
            pygame.display.quit()
            pygame.quit()
