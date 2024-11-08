import pygame
import sys
from holidays.halloween import Halloween
import random
from datetime import datetime

running = True

setting = Halloween().createSetting()
player = Halloween().createPlayer()
boss = Halloween().createBoss()

key_start = None
move = False
right = True
start_time = None
duration = 0
attack = False
boss_upload_time = float(random.randint(2,5))

while running:

    if start_time == None:

        start_time = datetime.now()

    if duration > boss_upload_time:

        attack = True
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
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                move = False

        
    setting

    player.updatePosition(move, right)
    player.drawPlayer(setting)
    boss.drawBoss(setting, attack)
    attack = False
    
    if start_time != None:
        duration = (datetime.now() - start_time).total_seconds()
        
    pygame.display.flip()

pygame.quit()
sys.exit()
