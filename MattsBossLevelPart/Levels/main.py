import pygame
import sys
from holidays.halloween import Halloween
from datetime import datetime

running = True

setting = Halloween().createSetting()
player = Halloween().createPlayer()
boss = Halloween().createBoss()

key_start = None
duration = 0
right = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                running = False
            elif event.key == pygame.K_RIGHT:
                key_start = datetime.now()
                right = True
            elif event.key == pygame.K_LEFT:
                right = False
                key_start = datetime.now()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                if key_start != None:
                    duration = (datetime.now() - key_start).total_seconds()
                    key_start = None

        
    setting
    player.updatePosition(duration, right)
    duration = 0
    player.drawPlayer(setting)
    
    boss.drawBoss(setting)
    pygame.display.flip()

pygame.quit()
sys.exit()
