import pygame
import sys
from holidays.halloween import Halloween
from datetime import datetime

running = True

setting = Halloween().createSetting()
player = Halloween().createPlayer()
boss = Halloween().createBoss()

key_start = None
move = False
right = True

while running:
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
    
    boss.drawBoss(setting)
    pygame.display.flip()

pygame.quit()
sys.exit()
