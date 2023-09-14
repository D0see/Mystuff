import pygame
import os
import sys
import random

pygame.init()

from core_variables import*
from collections import deque


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SHMUP')

def screen_flashes(clock, color, duration):
    for i in range(duration):
        clock.tick(FPS)
        WIN.fill(color)  
        pygame.display.update()
    
    
def draw_window(player_ship, background, background2, player_lives, player_won, current_boss, boss_is_hurt, *_):
    #player_health_display = HEALTHDISP_FONT.render("<3 "*player_lives, 1, WHITE)
  
    WIN.fill(BLACK)
    draw_background(background, background2)
    WIN.blit(player_ship.image, (player_ship.position[0] - 1/2*player_ship.deadzone, player_ship.position[1] - 1/2*player_ship.deadzone))
    #WIN.blit(player_health_display, (25, HEIGHT - player_health_display.get_height() - 20))
    if boss_is_hurt == False :
        current_boss.draw_bottom(WIN)
        boss_name_display = BOSS_NAME_DISPLAY_FONT.render(f'{current_boss.name.upper()}', 1, WHITE)
    else :
        current_boss.draw_bottom_hurt(WIN)
        boss_name_display = BOSS_NAME_DISPLAY_FONT.render(f'{current_boss.name.upper()}', 1, BLACK)
    for bullet in PLAYER_BULLETS:
        WIN.blit(PLAYERBULLET_IMAGE, (bullet.position[0], bullet.position[1]))
    for bullet in ENEMY_BULLETS:
        WIN.blit(ENEMYBULLET_IMAGE, (bullet[0].x, bullet[0].y))
    if boss_is_hurt == False :
        current_boss.draw_top(WIN)
    else :
        current_boss.draw_top_hurt(WIN)
    WIN.blit(boss_name_display, (WIDTH/2 - boss_name_display.get_width()/2, 10))
    if current_boss.health > 0 :
        dynamic_boss_health = pygame.transform.scale(BOSSHEALTH_AMOUNT_IMAGE, (703* current_boss.health/current_boss.max_health, 12))
        WIN.blit(dynamic_boss_health, (53, 54))
        WIN.blit(BOSSHEALTH_BORDER_IMAGE, (50, 50))
    # mask_image = current_boss.mask.to_surface()
    # WIN.blit(mask_image, (0,0))
    #pygame.draw.rect(WIN, WHITE, (current_boss.position[0], current_boss.position[1], current_boss.width, current_boss.height))
    pygame.display.update()

background_list = []
def draw_background(background, background2):
    background.y += BACKGROUND_VEL
    background2.y += BACKGROUND_VEL 
    if background.y >= 1000 :
        background.y = -4580
    if background2.y >= 1000:
        background2.y = -4580
    for background in background_list :
        WIN.blit(BACKGROUND_IMAGE, (background.x, background.y))

def introduction(intro, clock, player_ship, background, background2, current_boss):
    while intro == True :
        clock.tick(FPS)
        player_ship.position[1] -= player_ship.velocity
        # I don't get why this doesn't work
        #player_ship.draw(WIN)
        WIN.fill(BLACK)  
        draw_background(background, background2)
        WIN.blit(player_ship.image, (player_ship.position[0] - 1/2*player_ship.deadzone, player_ship.position[1] - 1/2*player_ship.deadzone))
        pygame.display.update()
        if player_ship.position[1] <= 800 :
            while current_boss.position[1] <= -3:
                clock.tick(FPS)
                WIN.fill(BLACK)  
                draw_background(background, background2)
                current_boss.draw(WIN)
                WIN.blit(player_ship.image, (player_ship.position[0] - 1/2*player_ship.deadzone, player_ship.position[1] - 1/2*player_ship.deadzone))
                current_boss.move_down(2)
                pygame.display.update()
                if current_boss.position[1] >= -5 : #FLASHES THE SCREEN WHITE
                    screen_flashes(clock, WHITE, 1)
            return False
        
def boss_outro(clock, background, background2, player_ship, previous_boss, current_boss): 
    outro = True
    while outro == True :
        while previous_boss.position[1] > (-previous_boss.height):
            clock.tick(FPS)
            WIN.fill(BLACK)  
            draw_background(background, background2)
            WIN.blit(player_ship.image, (player_ship.position[0] - 1/2*player_ship.deadzone, player_ship.position[1] - 1/2*player_ship.deadzone))       
            previous_boss.draw(WIN)
            previous_boss.move_up(3)
            pygame.display.update()

        if len(LIST_OF_BOSSES) == 1 :
            while player_ship.position[1]  > -40 :
                clock.tick(FPS)
                player_ship.position[1]  -= player_ship.velocity
                WIN.fill(BLACK)  
                draw_background(background, background2)
                player_win_display = HEALTHDISP_FONT.render("YOU SAVED THE WORLD ! GOOD JOB !", 1, WHITE)
                WIN.blit(player_win_display, (WIDTH/2 - player_win_display.get_width()/2, HEIGHT/2))
                WIN.blit(player_ship.image, (player_ship.position[0] - 1/2*player_ship.deadzone, player_ship.position[1] - 1/2*player_ship.deadzone))
                pygame.display.update()

            pygame.quit()
            sys.exit()
        
        while current_boss.position[1] <= -3:
                clock.tick(FPS)
                WIN.fill(BLACK)  
                draw_background(background, background2)
                current_boss.draw(WIN)
                WIN.blit(player_ship.image, (player_ship.position[0] - 1/2*player_ship.deadzone, player_ship.position[1] - 1/2*player_ship.deadzone))
                current_boss.move_down(2)
                pygame.display.update()
                if current_boss.position[1] >= -5 : #FLASHES THE SCREEN WHITE
                    screen_flashes(clock, WHITE, 1)

        outro = False
            

def player_movement(clock, player_ship, keys_pressed):
    movement_speed = player_ship.velocity
    #FOCUS MODE
    if keys_pressed[pygame.K_LCTRL] :
        movement_speed = round(player_ship.velocity/2)
    #MOVEMENT
    if keys_pressed[pygame.K_UP] and (player_ship.position[1]  - player_ship.velocity) > 130 :
        player_ship.position[1]  -= movement_speed
    if keys_pressed[pygame.K_DOWN] and (player_ship.position[1]  + player_ship.velocity) < 1000 - player_ship.height :
        if movement_speed == round(player_ship.velocity):
            player_ship.position[1]  += movement_speed + 1
        else :
            player_ship.position[1]  += movement_speed
    if keys_pressed[pygame.K_LEFT] and (player_ship.position[0] - player_ship.velocity) > 0 :
        player_ship.position[0] -= movement_speed
    if keys_pressed[pygame.K_RIGHT] and (player_ship.position[0] + player_ship.velocity) < 810 - player_ship.height :
        player_ship.position[0] += movement_speed
    #DEVGUN
    if keys_pressed[pygame.K_SPACE] and clock:
        time = pygame.time.get_ticks()/19
        if int(str(round(time))[-1]) == 5 :
            PLAYER_BULLETS.append(player_ship.weapon('playerbullet', PLAYERBULLET_HEIGHT, PLAYERBULLET_WIDTH, player_ship.position[0]+ 5, player_ship.position[1] - 10, PLAYERBULLET_VELOCITY, PLAYERBULLET_DAMAGE, PLAYERBULLET_IMAGE ))
            #PLAYER_BULLETS.append(pygame.Rect(player_ship.position[0]+ 5, player_ship.position[1] , 5, 5))
            


PLAYER_BULLETS = []   
ENEMY_BULLETS = []
def handle_bullets (player_ship, current_boss):
    def handle_player_bullets():
        for bullet in PLAYER_BULLETS :
            bullet.position[1] -= 8
            if bullet.position[1] <= 0:
                PLAYER_BULLETS.remove(bullet)
            for bosshitbox in current_boss.hitbox():
                if bullet.hitbox().colliderect(bosshitbox):
                    pygame.event.post(pygame.event.Event(BOSS_IS_HIT))
                    PLAYER_BULLETS.remove(bullet)
                    break

    handle_player_bullets()
    def handle_enemy_bullets():
        player_hitbox = player_ship.hitbox()
        for bullet in ENEMY_BULLETS :
            if player_hitbox.colliderect(bullet[0]):
                pygame.event.post(pygame.event.Event(PLAYER_IS_HIT))
                ENEMY_BULLETS.remove(bullet)
            bullet[0].y += bullet[1][1]
            bullet[0].x += bullet[1][0]
            if bullet[0].y > 1000:
                ENEMY_BULLETS.remove(bullet)
            
    handle_enemy_bullets()

def pattern_1(number_of_bullets, gap, bullet_starting_y):#gap is a tuple of 2 x position
    for _ in range(number_of_bullets):
        bullet_x_speed = random.randint(-4, 4)
        bullet_y_speed = 9 - abs(bullet_x_speed)
        bullet = (pygame.Rect((random.randint(*gap), bullet_starting_y, ENEMYBULLET_HEIGHT, ENEMYBULLET_WIDTH)),(bullet_x_speed, bullet_y_speed))
        ENEMY_BULLETS.append(bullet)

def pattern_2(startpoint):
    bullet_starting_x = startpoint[0]
    bullet_starting_y = startpoint[1]
    bullet_y_speed = 3
    bullet_x_speed = random.randint(-1, 1)
    bullet = (pygame.Rect((bullet_starting_x, bullet_starting_y, ENEMYBULLET_HEIGHT, ENEMYBULLET_WIDTH)),(bullet_x_speed, bullet_y_speed))
    return bullet

def pattern_3(startpoint, player_ship):
    bullet_starting_x = startpoint[0]
    bullet_starting_y = startpoint[1]
    bullet_y_speed = 10
    bullet_x_speed = (-1*(startpoint[0] - player_ship.position[0]))*1/(player_ship.position[1] / bullet_y_speed)
    bullet = (pygame.Rect(bullet_starting_x, bullet_starting_y, ENEMYBULLET_HEIGHT, ENEMYBULLET_WIDTH)),(bullet_x_speed, bullet_y_speed)
    return bullet

LIST_OF_BOSSES =  deque([None, HOMONCULUSVENER, bosstest, boss1]) #MUST START WITH NONE
current_boss = LIST_OF_BOSSES[-1]
running = True 
def main(running):
    global PLAYER_BULLETS
    global ENEMY_BULLETS
    global LIST_OF_BOSSES
    global current_boss
    intro = True
    background, background2 = pygame.Rect(0,-1790,BACKGROUND_WIDTH, BACKGROUND_HEIGHT), pygame.Rect(0,-4580,BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
    background_list.append(background)
    background_list.append(background2)
    player_ship = starting_ship
    clock = pygame.time.Clock()
    

    PLAYER_LIVES = 1
    player_won = False
    boss_pattern_counter = 0
    boss_internal_clock = 0
    pattern_2_activated, pattern_2_counter = False, 0
    pattern_3_activated, pattern_3_counter = False, 0
    while running :
        boss_is_hurt = False

        clock.tick(FPS)

        while intro == True :
            intro = introduction(intro, clock, player_ship, background, background2, current_boss)

        if intro == False :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_SPACE :
                        #PLAYER_BULLETS.append(pygame.Rect(player_ship.position[0]+ 5, player_ship.position[1] , 5, 5))
                        pass
                    if event.key == pygame.K_a :
                        pass
                    if event.key == pygame.K_z :
                        pass
                    if event.key == pygame.K_e :
                        pass
                
                if event.type == PLAYER_IS_HIT :
                    PLAYER_LIVES -= 1
                if PLAYER_LIVES == 0 :
                    pygame.quit()
                    sys.exit()
                if event.type == BOSS_IS_HIT :
                    current_boss.health -= PLAYERBULLET_DAMAGE
                    boss_is_hurt = True
                if current_boss.health <= 0 :
                    player_won = True

            if player_won == True :
                if len(LIST_OF_BOSSES) > 1 :
                    player_won = False
                    previous_boss = LIST_OF_BOSSES.pop()
                    current_boss = LIST_OF_BOSSES[-1]
                    
                    
                    boss_outro(clock, background, background2, player_ship, previous_boss, current_boss)
                    boss_pattern_counter = 0
                    boss_internal_clock = 0
                    PLAYER_BULLETS = []   
                    ENEMY_BULLETS = []
                 
            if boss_internal_clock >= current_boss.wait_time :
                pattern_num = current_boss.pattern[boss_pattern_counter]
                boss_pattern_counter +=1
                boss_internal_clock = 0
                if pattern_num == 1 :
                    pattern_1(15,current_boss.gap, current_boss.pattern1_y_start)
                if pattern_num == 2 :
                    pattern_2_activated = True
                    startpoint = current_boss.startingpoints_pattern2[random.randint(0,len(current_boss.startingpoints_pattern2)-1)]
                if pattern_num == 3 :
                    pattern_3_activated = True
                    startpoint = current_boss.startingpoint_pattern3
                    
            boss_internal_clock += 1
                

            if pattern_2_activated == True :
                if boss_internal_clock % 2 == 0 :
                    ENEMY_BULLETS.append(pattern_2(startpoint))
                    pattern_2_counter += 1
                if pattern_2_counter == current_boss.wait_time:
                    pattern_2_activated = False 
                    pattern_2_counter = 0
            if pattern_3_activated == True :
                ENEMY_BULLETS.append(pattern_3(startpoint, player_ship))
                pattern_3_counter += 1
                if pattern_3_counter == 10:
                    pattern_3_activated = False 
                    pattern_3_counter = 0
        

                        

        keys_pressed = pygame.key.get_pressed()
        handle_bullets(player_ship, current_boss)
        player_movement(clock, player_ship, keys_pressed)
        draw_window(player_ship, background, background2, PLAYER_LIVES, player_won, current_boss, boss_is_hurt)

    pygame.quit()
    sys.exit()




if __name__ == '__main__' :
    main(running)