import pygame
from entities import Player, Enemy, RoadMarker,Finish
import settings as s
import agent as a
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN, 
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Game:
    """Provides game flow."""

    def __init__(self, screen, clock):
        self.screen          = screen        
        self.clock           = clock
        
        self.seed            = s.SEED
        self.window          = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT))

        self.player          = Player()
        self.agent           = a.Agent()
        self.finish_line     = Finish()

        self.enemies         = pygame.sprite.Group()
        self.all_sprites     = pygame.sprite.Group()
        self.roadmarkers     = pygame.sprite.Group()
        
        self.running         = True
        self.paused          = False
        self.ticks           = 0
        self.crashes         = 0
        self.obs_index       = 0
        self.marker_index = 0

        self.all_sprites.add(self.finish_line)
        self.all_sprites.add(self.player)
        self.obstacles_x, self.obstacles_y = self._generate_obstacle_coords(self.seed)
        self.road_marker_x, self.road_marker_y = self._generate_roadmarker_coords()

    def update(self):

        self._add_road_markers()
        self._add_enemies()
        states = self._get_states()
        u_x, u_y = self._get_actions(states)

        self.player.update(u_x, u_y)
        self.enemies.update(self.player.s_y)
        self.finish_line.update(self.player.s_y)
        self.roadmarkers.update(self.player.s_y)
        self._handle_collisions()
        self._check_finished()
        
        self.ticks += 1
        # Ensure we maintain a 30 frames per second rate
        self.clock.tick(s.FPS)
        
        if s.DEBUG:
            print(f"fps: {self.clock.get_fps()}")
    
    
    def render(self):
        # Fill the screen with sky blue
        red = max(0,min(255, self.player.v_y*5))
        self.window.fill((red, 255, 255-red))
        
        # Draw all our sprites
        for entity in self.all_sprites:
            self.window.blit(entity.surf, entity.rect)

        font = pygame.font.SysFont('Arial', 12)
        fps = font.render(f"FPS: {round(self.clock.get_fps(),2)}", True, (0,0,0))
        speed = font.render(f"Speed: {round(self.player.v_y,1)}",True,(0,0,0))
        ticks = font.render(f"Ticks: {self.ticks}",True,(0,0,0))
        self.window.blit(fps,(s.WINDOW_WIDTH-80,20))
        self.window.blit(speed, (s.WINDOW_WIDTH - 80, 40))
        self.window.blit(ticks, (s.WINDOW_WIDTH - 80, 60))

        self.screen.fill(s.BLACK)
        self.screen.blit(self.window, ((s.SCREEN_WIDTH-s.WINDOW_WIDTH)/2, (s.SCREEN_HEIGHT-s.WINDOW_HEIGHT)/2))
        
        # pygame.draw.rect(window, RED, (0, 800, 0, 100))
        # Flip everything to the display
        pygame.display.update()
        
    
    def _get_states(self):
        
        return  self.enemies.sprites()
    
    
    def _add_enemies(self):
        
        while (self.obs_index < s.NUM_OBSTACLES) and (self.player.s_y + s.HORIZON > self.obstacles_y[self.obs_index]):
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy(s_x = self.obstacles_x[self.obs_index], s_y = self.obstacles_y[self.obs_index])
            self.enemies.add(new_enemy)
            self.all_sprites.add(new_enemy)
            
            self.obs_index += 1

    def _add_road_markers(self):

        while (self.marker_index < s.TRACK_LENGTH) and (self.player.s_y + s.HORIZON > self.road_marker_y[self.marker_index]):
            # Create the new enemy, and add it to our sprite groups
            new_marker_left = RoadMarker(s_x=self.road_marker_x[self.marker_index], s_y=self.road_marker_y[self.marker_index])
            new_marker_right = RoadMarker(s_x=self.road_marker_x[self.marker_index+1],
                                         s_y=self.road_marker_y[self.marker_index+1])

            self.roadmarkers.add(new_marker_left)
            self.roadmarkers.add(new_marker_right)
            self.all_sprites.add(new_marker_left)
            self.all_sprites.add(new_marker_right)

            self.marker_index += 2
            
            
    def _get_actions(self, states):
        
        u_x = u_y = 0
        
        pressed_keys = pygame.key.get_pressed()
        if s.RENDER and any(pressed_keys):
            if pressed_keys[K_UP]:
                u_y = 1
                # move_up_sound.play()
            if pressed_keys[K_DOWN]:
                u_y = -1
                # move_down_sound.play()
            if pressed_keys[K_LEFT]:
                u_x = -1
            if pressed_keys[K_RIGHT]:
                u_x = 1

        else:
            u_x, u_y = self.agent.act(states)

        return u_x, u_y
    
    
    def _handle_collisions(self):
        
        collided = pygame.sprite.spritecollideany(self.player, self.enemies)
        # Check if any enemies have collided with the player
        if collided:
            # If so, remove the player
            self.player.penalize()
            collided.kill()
            self.crashes += 1
            # Stop any moving sounds and play the collision sound
            # move_up_sound.stop()
            # move_down_sound.stop()
            # collision_sound.play()
    
            # Stop the loop
            # running = False    
            
            
    def _check_finished(self):
        
        if self.player.s_y > s.TRACK_LENGTH:

            self.running = False
            
    def _generate_obstacle_coords(self, seed=0):
        
        random.seed(seed)
        obstacles_y = [0]
        for i in range(s.NUM_OBSTACLES):
            randint = random.randint(100,200)
            obstacles_y.append(obstacles_y[i] + randint)

        obstacles_y = [x/obstacles_y[-1]*(s.TRACK_LENGTH-s.SPAWN_AREA)+s.SPAWN_AREA for x in obstacles_y][:-1]
        obstacles_x = [random.randint(0.5*s.ENEMY_SIZE[0], s.WINDOW_WIDTH - 1.5*s.ENEMY_SIZE[0]) for x in range(len(obstacles_y))]

        return obstacles_x, obstacles_y

    def _generate_roadmarker_coords(self):

        marker_y = []
        marker_x = []
        for i in range(int(s.TRACK_LENGTH)):
            marker_y.append(i*125)
            marker_x.append(s.WINDOW_WIDTH*0.25)

            marker_y.append(i*125)
            marker_x.append(s.WINDOW_WIDTH*0.75)
        return marker_x, marker_y
