from abstract.boss import Boss
import pygame
import torch
from .boss_attacks import BossAttacks

class FearThePumpkin(Boss):

    def __init__(self):

        self.position = (700,399)
        self.boss_surface = pygame.Surface((100,100))
        self.all_attacks = []
        self.p_surface = pygame.Surface((250, 30))
        self.p_surface.fill((0,0,0))
        self.image = pygame.image.load("MattsBossLevelPart/Levels/bosses/pumpkin.png")
        self.scaled_img = pygame.transform.scale(self.image, (80,80))



    def getPosition(self):

        pass
    
    def setPosition(self):

        pass

    def drawBoss(self, setting, attack):

        
        # pygame.draw.circle(self.boss_surface, (255,255,255), (50,75), 25)
        self.boss_surface.blit(self.scaled_img, (10,20))
        setting.blit(self.boss_surface, self.position)
        pygame.draw.rect(self.p_surface, (255,165,0), (0,0,250,30))
        setting.blit(self.p_surface, (525,25))

        if attack:

            ba = BossAttacks()
            ba.initializeAttack(setting, 1)
            self.all_attacks.append(ba)

    def getBossAttacks(self):

        return self.all_attacks
    
    def clearAttackList(self):

        self.all_attacks = []



    
