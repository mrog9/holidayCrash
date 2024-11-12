import pygame
import sys
from holidays.halloween import Halloween
import random
from datetime import datetime
from all_attacks import AllAttacks

running = True

h_obj = Halloween()
b_attacks = AllAttacks()

setting =h_obj.createSetting()
player = h_obj.createPlayer()
boss = h_obj.createBoss()

key_start = None
move = False
right = True
start_time = None
duration = 0
p_power = 0.0
b_attack = False
b_IS_alive = True
boss_upload_time = float(random.randint(2,5))
p_IS_alive = True
p_start = None
p_attack = False
power_up = False

while running:

    if start_time == None:

        start_time = datetime.now()

    if duration > boss_upload_time:

        b_attack = True
        duration = 0.0
        start_time = None
        boss_upload_time = float(random.randint(2,5))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                running = False
            elif event.key == pygame.K_RIGHT:
                move = True
                right = True
            elif event.key == pygame.K_LEFT:
                right = False
                move = True
            elif event.key == pygame.K_UP:
                power_up = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                move = False
            elif event.key == pygame.K_UP:
                p_attack = True
                power_up = False

    setting
      

    
    boss.drawBoss(setting, b_attack)
    player.updatePosition(move, right)
    p_IS_alive, b_IS_alive = b_attacks.updateAll(setting, boss, player)
    player.drawPlayer(setting, p_attack, p_power)

    if power_up:
        p_power += .0002
    else:
        p_power = 0

    if not p_IS_alive or not b_IS_alive:

        running = False
    
    
    b_attack = False
    p_attack = False
    
    if start_time != None:
        duration = (datetime.now() - start_time).total_seconds()

    setting = h_obj.createSetting()
        
    pygame.display.flip()

running = True

while running:

    if b_IS_alive:
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        setting.fill((0,0,0))
        text1 = "YOU HAVE BEEN DEFEATED!"
        text2 = "Press ESC to go to leaderboard"
        text_surf1 = font.render(text1, True, (255,165,0))
        text_surf2 = font.render(text2, True, (200,0,0))
        setting.blit(text_surf1, (200,200))
        setting.blit(text_surf2, (200,300))
    else:
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        setting.fill((0,0,0))
        text1 = "YOU HAVE WON!!!!"
        text2 = "Press ESC to go to next level"
        text_surf1 = font.render(text1, True, (200,200,200))
        text_surf2 = font.render(text2, True, (0,0,200))
        setting.blit(text_surf1, (200,200))
        setting.blit(text_surf2, (200,300))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                running = False

    pygame.display.flip()


pygame.quit()
sys.exit()
