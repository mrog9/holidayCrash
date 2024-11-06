import pygame
import sys
from holidays.halloween import Halloween

running = True

setting = Halloween().createSetting()
player = Halloween().createPlayer()
boss = Halloween().createBoss()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                running = False
        
    setting
    player.drawPlayer(setting)
    boss.drawBoss(setting)
    pygame.display.flip()

pygame.quit()
sys.exit()
