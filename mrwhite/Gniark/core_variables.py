import pygame
import os
from collections import deque


pygame.init()

WIDTH, HEIGHT = 810, 1000

FPS = 60

    #EVENTS
PLAYER_IS_HIT = pygame.USEREVENT + 1
BOSS_IS_HIT = pygame.USEREVENT + 2

    #BACKGROUND
BACKGROUND_IMAGE = pygame.image.load(os.path.join('assets', 'background.png'))
BACKGROUND_HEIGHT, BACKGROUND_WIDTH = 2790, 810
BACKGROUND_VEL = 1
    #PLAYER HEALTH DISPLAY
HEALTHDISP_FONT = pygame.font.SysFont('IMPACT', 40)
    #BOSS NAME DISPLAY
BOSS_NAME_DISPLAY_FONT = pygame.font.SysFont('IMPACT', 30)
    #BOSS HEALTH DISPLAY
BOSSHEALTH_BORDER_IMAGE = pygame.image.load(os.path.join('assets', 'healthbarholder.png'))
BOSSHEALTH_AMOUNT_IMAGE = pygame.image.load(os.path.join('assets', 'healthbar.png'))
    #COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

    #ENTITIES 

#BULLETS 
class Bullet(pygame.sprite.Sprite):
    bullet_counter = 0
    def __init__(self, name, height, width, x, y, velocity, damage, image ) -> None:
        Bullet.bullet_counter += 1
        super().__init__()
        self.name = name + str(Bullet.bullet_counter)
        self.height = height
        self.width = width
        self.position = [x,y]
        self.velocity = velocity
        self.damage = damage
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def hitbox(self):
        return pygame.Rect(self.position[0], self.position[1], self.height, self.width)


PLAYERBULLET_HEIGHT, PLAYERBULLET_WIDTH = 5, 5
PLAYERBULLET_IMAGE = pygame.image.load(os.path.join('assets','player_bullet.png'))
PLAYERBULLET_MASK = pygame.mask.from_surface(PLAYERBULLET_IMAGE)
PLAYERBULLET_DAMAGE = 8
PLAYERBULLET_VELOCITY = 8

ENEMYBULLET_HEIGHT, ENEMYBULLET_WIDTH = 32, 32
ENEMYBULLET_IMAGE = pygame.image.load(os.path.join('assets', 'enemy_bullet.png'))


    #PLAYABLE SHIPS

class Ship(pygame.sprite.Sprite):
    def __init__(self, name, height, width, x, y, velocity, deadzone, reload_time, reload_counter, image, weapon) -> None:
        super().__init__()
        self.name = name 
        self.height = height 
        self.width = width 
        self.position = [x,y]
        self.velocity = velocity
        self.deadzone = deadzone
        self.reload_time = reload_time
        self.reload_counter = reload_counter
        self.image = image
        self.weapon = weapon


    def hitbox(self):
        return pygame.Rect(self.position[0], self.position[1], self.height-self.deadzone, self.width-self.deadzone)
    
    def draw(self, surface): #somehow doesn't work
        surface.blit(self.image, [self.position[0] - 1/2*self.deadzone, self.position[1] - 1/2*self.deadzone])
        
#STARTING_SHIP
STARTINGSHIP_NAME = 'startingship'
STARTINGSHIP_HEIGHT, STARTINGSHIP_WIDTH = 32, 32
STARTINGSHIP_IMAGE = pygame.image.load(os.path.join('assets', 'playership.png'))
STARTINGSHIP_HIT_IMAGE = pygame.image.load(os.path.join('assets', 'playership.png'))
STARTINGSHIP_VEL = 5
STARTINGSHIP_DEADZONE = 16
STARTINGSHIP_RELOADTIME = 12
STARTINGSHIP_RELOADCOUNTER = 0

starting_ship = Ship(STARTINGSHIP_NAME, STARTINGSHIP_HEIGHT, STARTINGSHIP_WIDTH, WIDTH/2, HEIGHT, STARTINGSHIP_VEL, 
                     STARTINGSHIP_DEADZONE, STARTINGSHIP_RELOADTIME, STARTINGSHIP_RELOADCOUNTER, STARTINGSHIP_IMAGE, Bullet)
        

    #BOSSES

class Boss(pygame.sprite.Sprite):
    def __init__(self, name, height, width, x, y, velocity_x, velocity_y, health, max_health, pattern_list, wait_time, image, bottom_image, top_image, 
                 hurt_top_image, hurt_bottom_image) -> None:
        super().__init__()
        self.name = name
        self.health = health
        self.height = height
        self.max_health = max_health
        self.width = width
        self.velocity = [velocity_x, velocity_y]
        self.position = [x,y]
        self.pattern = pattern_list
        self.wait_time = wait_time
        self.image = image
        self.bottom_image = bottom_image
        self.top_image = top_image
        self.hurt_top_image = hurt_top_image
        self.hurt_bottom_image = hurt_bottom_image
        self.mask = pygame.mask.from_surface(self.image)

    def hitbox(self):
        return [pygame.Rect(self.position[0], self.position[1], self.width, self.height)]
    
    def update(self):
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def draw(self, surface):
        surface.blit(self.image, self.position)

    def draw_top(self, surface):
        surface.blit(self.top_image, self.position)

    def draw_bottom(self, surface):
        surface.blit(self.bottom_image, [self.position[0], self.position[1]])

    def draw_top_hurt(self, surface):
        surface.blit(self.hurt_top_image, self.position)

    def draw_bottom_hurt(self, surface):
        surface.blit(self.hurt_bottom_image, [self.position[0], self.position[1]])
    
    def move_up(self, vel):
        self.velocity[1] -= vel
        self.update()
        self.velocity[1] = 0

    def move_down(self, vel):
        self.velocity[1] += vel
        self.update()
        self.velocity[1] = 0

    def retreat(self, vel):
        while (self.position[1] + self.height) > 0 :
            self.move_up(vel)

    #BOSS1

class Homonculus(Boss):
    def __init__(self, name, height, width, x, y, velocity_x, velocity_y, health, max_health, pattern_list, wait_time, image, bottom_image, top_image, hurt_top_image, hurt_bottom_image,) -> None:
        super().__init__(name, height, width, x, y, velocity_x, velocity_y, health, max_health, pattern_list, wait_time, image, bottom_image, top_image, hurt_top_image, hurt_bottom_image)
    
    def hitbox(self):
        return [pygame.Rect(self.position[0], self.position[1], self.width, 25), pygame.Rect(self.position[0] + 25, self.position[1], self.width -25, 100), 
                pygame.Rect(self.position[0] + 75, self.position[1], self.width -75, 150), pygame.Rect(self.position[0] + 110, self.position[1], self.width -110, 175),
                pygame.Rect(self.position[0] + 150, self.position[1], self.width -150, 200),pygame.Rect(self.position[0] + 200, self.position[1], self.width -200, 225),
                pygame.Rect(self.position[0] + 225, self.position[1], self.width -225, 230), pygame.Rect(self.position[0] + 275, self.position[1], self.width -275, 235),
                pygame.Rect(self.position[0] + 300, self.position[1], self.width -300, 245)]
#BOSS1
BOSS1_NAME = 'Homonculus'
BOSS1_IMAGE = pygame.image.load(os.path.join('assets', 'BOSS1.png'))
BOSS1_TOP_IMAGE = pygame.image.load(os.path.join('assets', 'homonculusnoirtophalf.png'))
BOSS1_BOTTOM_IMAGE = pygame.image.load(os.path.join('assets', 'homonculusnoirbottomhalf.png'))
BOSS1_HURT_TOP_IMAGE =  pygame.image.load(os.path.join('assets', 'homonculushurttophalf.png'))
BOSS1_HURT_BOTTOM_IMAGE = pygame.image.load(os.path.join('assets', 'homonculushurtbottomhalf.png'))
BOSS1_HEIGHT, BOSS1_WIDTH = 250, 810
BOSS1_STARTINGPOINT = 0, -250
BOSS1_PATTERN_LIST = [1, None, None, 2, None, None, 2, 2] + [None, None, 1, 3, None, 2, 1, None, 1, 2, None, 3, 3, 
                                                             3]*2 + [None] + [3, 2, 3, 3, 3, 1, 1, 3, None, 2, 1, None, 1, 2, None, 3, 3, 3]*4
BOSS1_WAIT = 70
BOSS1_MAXHEALTH = 1000
BOSS1_HEALTH = 1000
BOSS1_PATTERN_STARTING_Y = 20


boss1 = Homonculus(BOSS1_NAME, BOSS1_HEIGHT, BOSS1_WIDTH, BOSS1_STARTINGPOINT[0], BOSS1_STARTINGPOINT[1], 0, -BOSS1_HEIGHT, BOSS1_HEALTH, BOSS1_MAXHEALTH, BOSS1_PATTERN_LIST, 
             BOSS1_WAIT, BOSS1_IMAGE, BOSS1_BOTTOM_IMAGE, BOSS1_TOP_IMAGE, BOSS1_HURT_TOP_IMAGE, BOSS1_HURT_BOTTOM_IMAGE)


#PATTERN1
boss1.gap = (125, 685)
boss1.pattern1_y_start = BOSS1_PATTERN_STARTING_Y
#PATTERN2
boss1.startingpoints_pattern2 = [(WIDTH/3, BOSS1_PATTERN_STARTING_Y),(WIDTH/3*2, BOSS1_PATTERN_STARTING_Y)]
#PATTERN3
boss1.startingpoint_pattern3 = (boss1.gap[0]+ boss1.gap[1])/2, BOSS1_PATTERN_STARTING_Y

#BOSSTEST
BOSSTEST_NAME = 'Homonculus AGACÉ'
BOSSTEST_IMAGE = pygame.image.load(os.path.join('assets', 'homonculusorange.png'))
BOSSTEST_TOP_IMAGE = pygame.image.load(os.path.join('assets', 'homonculusorangetophalf.png'))
BOSSTEST_BOTTOM_IMAGE = pygame.image.load(os.path.join('assets', 'homonculusorangebottomhalf.png'))
BOSSTEST_HURT_TOP_IMAGE =  pygame.image.load(os.path.join('assets', 'homonculushurttophalf.png'))
BOSSTEST_HURT_BOTTOM_IMAGE = pygame.image.load(os.path.join('assets', 'homonculushurtbottomhalf.png'))
BOSSTEST_HEIGHT, BOSSTEST_WIDTH = 250, 810
BOSSTEST_STARTINGPOINT = 0, -250
BOSSTEST_PATTERN_LIST = [1, 3, 2, 2, 1, None, 1, 2, 1, 3, 3, 3, 2] + [3, 2, 3, 3, 3, 1, 1, 3, 2, 2, 1, 1, 2, None, 3, 3, 3]*8
BOSSTEST_WAIT = 35
BOSSTEST_MAXHEALTH = 1250
BOSSTEST_HEALTH = 1250
BOSSTEST_PATTERN_STARTING_Y = 20

bosstest = Homonculus(BOSSTEST_NAME, BOSSTEST_HEIGHT, BOSSTEST_WIDTH, BOSSTEST_STARTINGPOINT[0], BOSSTEST_STARTINGPOINT[1], 0, -BOSSTEST_HEIGHT, BOSSTEST_HEALTH,
                BOSSTEST_MAXHEALTH, BOSSTEST_PATTERN_LIST, BOSS1_WAIT, BOSSTEST_IMAGE, BOSSTEST_BOTTOM_IMAGE, BOSSTEST_TOP_IMAGE, BOSSTEST_HURT_TOP_IMAGE, 
                BOSSTEST_HURT_BOTTOM_IMAGE)

#PATTERN1
bosstest.gap = (125, 685)
bosstest.pattern1_y_start = BOSSTEST_PATTERN_STARTING_Y
#PATTERN2
bosstest.startingpoints_pattern2 = [(WIDTH/3, BOSSTEST_PATTERN_STARTING_Y),(WIDTH/3*2, BOSSTEST_PATTERN_STARTING_Y)]
#PATTERN3
bosstest.startingpoint_pattern3 = (bosstest.gap[0]+ bosstest.gap[1])/2, BOSSTEST_PATTERN_STARTING_Y

#BOSSTEST
HOMONCULUSVENER_NAME = 'Homonculus pas content'
HOMONCULUSVENER_IMAGE = pygame.image.load(os.path.join('assets', 'homonculusvener.png'))
HOMONCULUSVENER_TOP_IMAGE = pygame.image.load(os.path.join('assets', 'homonculusvenertophalf.png'))
HOMONCULUSVENER_BOTTOM_IMAGE = pygame.image.load(os.path.join('assets', 'homonculusvenerbottomhalf.png'))
HOMONCULUSVENER_HURT_TOP_IMAGE =  pygame.image.load(os.path.join('assets', 'homonculushurttophalf.png'))
HOMONCULUSVENER_HURT_BOTTOM_IMAGE = pygame.image.load(os.path.join('assets', 'homonculushurtbottomhalf.png'))
HOMONCULUSVENER_HEIGHT, HOMONCULUSVENER_WIDTH = 250, 810
HOMONCULUSVENER_STARTINGPOINT = 0, -250
HOMONCULUSVENER_PATTERN_LIST = [1, 3, 2, 1, 1, 1, 2, 1, 3, 1, 2, 3] + [1, 2, 1, 1, 1, 2, 1, 3, 2, 2, 1, 3, 1, 2, 3, 3, 3, 3]*8
HOMONCULUSVENER_WAIT = 30
HOMONCULUSVENER_MAXHEALTH = 1500
HOMONCULUSVENER_HEALTH = 1500
HOMONCULUSVENER_PATTERN_STARTING_Y = 20

HOMONCULUSVENER = Homonculus(HOMONCULUSVENER_NAME, HOMONCULUSVENER_HEIGHT, HOMONCULUSVENER_WIDTH, HOMONCULUSVENER_STARTINGPOINT[0], HOMONCULUSVENER_STARTINGPOINT[1], 0, -HOMONCULUSVENER_HEIGHT, HOMONCULUSVENER_HEALTH,
                HOMONCULUSVENER_MAXHEALTH, HOMONCULUSVENER_PATTERN_LIST, HOMONCULUSVENER_WAIT, HOMONCULUSVENER_IMAGE, HOMONCULUSVENER_BOTTOM_IMAGE, HOMONCULUSVENER_TOP_IMAGE, HOMONCULUSVENER_HURT_TOP_IMAGE, 
                HOMONCULUSVENER_HURT_BOTTOM_IMAGE)

#PATTERN1
HOMONCULUSVENER.gap = (125, 685)
HOMONCULUSVENER.pattern1_y_start = HOMONCULUSVENER_PATTERN_STARTING_Y
#PATTERN2
HOMONCULUSVENER.startingpoints_pattern2 = [(WIDTH/3, HOMONCULUSVENER_PATTERN_STARTING_Y),(WIDTH/3*2, BOSSTEST_PATTERN_STARTING_Y)]
#PATTERN3
HOMONCULUSVENER.startingpoint_pattern3 = (HOMONCULUSVENER.gap[0]+ bosstest.gap[1])/2, HOMONCULUSVENER_PATTERN_STARTING_Y



