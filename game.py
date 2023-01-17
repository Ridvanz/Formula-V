import pygame
import settings as s
import random

from simulate import game_update, get_initial_state   

from pygame.locals import ( K_UP,
                            K_DOWN, 
                            K_LEFT,
                            K_RIGHT)

class Game:
    """Provides game flow."""

    def __init__(self, seed):
        
        self.seed            = seed

        
        self.player, self.obstacles, self.idx =  get_initial_state()
        

        # self.player          = Player()
        # self.finish_line     = Finish()
        
        # self.enemies         = pygame.sprite.Group()
        # self.all_sprites     = pygame.sprite.Group()
        # self.roadmarkers     = pygame.sprite.Group()
        
        self.running           = True
        # self.paused          = False
        self.ticks             = 0
        self.finished          = False
        
        # self.crashes         = 0
        # self.obs_index       = 0
        # self.marker_index    = 0
        
        if s.RENDER:
        
            self.display = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
            pygame.display.set_caption("Formula V")
            self.clock = pygame.time.Clock()
                
            pygame.init()
            pygame.event.set_blocked (pygame.MOUSEMOTION )

            self.window  = pygame.Surface((s.WINDOW_WIDTH, s.WINDOW_HEIGHT))
            self.size = (0.05 * s.WINDOW_WIDTH, 0.05 * s.WINDOW_HEIGHT)
            
            if s.SOUND:
                pygame.mixer.init()
                pygame.mixer.music.load("assets/music/game.mp3")
                pygame.mixer.music.play(loops=-1)


    def update(self, action):
                
        if s.RENDER:
            u_x, u_y = self._get_control_input(action)
        
        self.player, self.obstacles, self.idx = game_update((u_x, u_y), self.player, self.obstacles, self.idx)
        
        if self.player[1] > 100:
            self.finished = True
        
        self.ticks += 1

        if s.DEBUG:
            print(f"fps: {self.clock.get_fps()}")
    
    def render(self):
        red = max(0,min(255, self.player[3]*5))
        self.window.fill((red, 255, 255-red))
        
        color = (0, 0, 0)
        player_surf = pygame.Surface(self.size)
        player_surf.fill(color)
        # player_rect = player_surf.get_rect()
        
        # print(player_rect)
        
        player_x = self.player[0] * (s.WINDOW_WIDTH-self.size[0])
        player_y = s.WINDOW_HEIGHT-2*self.size[1]
        
        self.window.blit(player_surf, (player_x,player_y))
         
        color = (255, 0, 0)
        obstacle_surf = pygame.Surface(self.size)
        obstacle_surf.fill(color)
        
        for i in range(self.obstacles.shape[0]):
            if self.obstacles[i, 3]:
                obstacle_x = self.obstacles[i, 0] * (s.WINDOW_WIDTH-self.size[0])
                obstacle_y = (2-self.obstacles[i, 1]) * (s.WINDOW_WIDTH-2*self.size[1])
                
                self.window.blit(obstacle_surf, (obstacle_x,obstacle_y))
         
        #text 
        text_color = (255,0,255)
        self.display.fill(s.BLACK)
        self.display.blit(self.window, ((s.SCREEN_WIDTH-s.WINDOW_WIDTH)/2, (s.SCREEN_HEIGHT-s.WINDOW_HEIGHT)/2))
        
        font = pygame.font.SysFont('Arial', 16)
        fps = font.render(f"FPS: {round(self.clock.get_fps(),2)}", True, text_color)
        speed = font.render(f"Speed: {round(self.player[3],1)}",True,text_color)
        ticks = font.render(f"Ticks: {self.ticks}",True,text_color)
        distance_left = font.render(f"Distance left: {(s.TRACK_LENGTH-self.player[1])}",True,text_color)
        
        text_x = s.WINDOW_WIDTH + (s.SCREEN_WIDTH-s.WINDOW_WIDTH)/2 + 5
        
        self.display.blit(fps,(text_x,20))
        self.display.blit(speed, (text_x, 60))
        self.display.blit(ticks, (text_x, 100))
        self.display.blit(distance_left,(text_x,140))
        
        pygame.display.update()
        
        self.clock.tick(s.FPS)
        
    def observe(self):
        
        # player = {}
        # player["left_wall"] = self.player.s_x+s.PLAYER_SIZE[0]/2
        # player["right_wall"] = s.WINDOW_WIDTH - self.player.s_x - s.PLAYER_SIZE[0]/2
        # player["distance_traveled"] = self.player.s_y
        # player["velocity_x"] = self.player.v_x
        # player["velocity_y"] = self.player.v_y
        
        # obstacles = []
        # for enemy in self.enemies.sprites():
        #     obstacle = {}
        #     obstacle["relative_x"] = enemy.s_x -  self.player.s_x
        #     obstacle["relative_y"] = enemy.s_y -  self.player.s_y - s.PLAYER_SIZE[1]
        #     obstacles.append(obstacle)
        
        states = {"player": self.player, "obstacles": self.obstacles}
        
        #print(states)
        return states
    
    # def wait(self):
        
    #     while self.paused: 
    #         pressed_keys = pygame.key.get_pressed()

    #         if pressed_keys[K_UP]:
    #             self.paused = False
    
    # def _add_enemies(self):
        
    #     while (self.obs_index < s.NUM_OBSTACLES) and (self.player.s_y + s.HORIZON > self.obstacles_y[self.obs_index]):

    #         new_enemy = Enemy(s_x = self.obstacles_x[self.obs_index], s_y = self.obstacles_y[self.obs_index])
    #         self.obstacles.add(new_enemy)
    #         self.all_sprites.add(new_enemy)
            
    #         self.obs_index += 1
            
    # def _add_road_markers(self):

    #     while (self.marker_index < s.TRACK_LENGTH) and (self.player.s_y + s.HORIZON > self.road_marker_y[self.marker_index]):

    #         new_marker = RoadMarker(s_x=self.road_marker_x[self.marker_index], s_y=self.road_marker_y[self.marker_index])
    #         self.roadmarkers.add(new_marker)
    #         self.all_sprites.add(new_marker)

    #         self.marker_index += 1

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
    
    
    def _handle_collisions(self):
        
        collided = pygame.sprite.spritecollideany(self.player, self.obstacles)

        if collided:

            self.player.penalize()
            collided.kill()
            self.crashes += 1
            # move_up_sound.stop()
            # move_down_sound.stop()
            # collision_sound.play()            
            
    def _check_finished(self):
        
        if self.player.s_y > s.TRACK_LENGTH:

            self.running = False
            
    def _generate_obstacle_coords(self, seed=0):
        if s.NUM_OBSTACLES > 0:
        
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
            marker_x.append(s.WINDOW_WIDTH*0.50)

            marker_y.append(i*125)
            marker_x.append(s.WINDOW_WIDTH*0.75)
        return marker_x, marker_y

    def _stop(self):
        if s.SOUND:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
    
        if s.RENDER:
            pygame.display.quit()
            pygame.quit()
            
