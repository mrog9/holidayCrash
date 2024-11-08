from abstract.boss import Boss
import pygame
import torch
from .boss_attacks import BossAttacks

class FearThePumpkin(Boss):

    def __init__(self):

        self.position = (700,399)
        self.boss_surface = pygame.Surface((100,100))
        self.all_attacks = pygame.sprite.Group()


    def getPosition(self):

        pass
    
    def setPosition(self):

        pass

    def drawBoss(self, setting, attack):

        if len(self.all_attacks)>0:

            self.all_attacks.update(setting)

        pygame.draw.circle(self.boss_surface, (255,255,255), (50,75), 25)
        setting.blit(self.boss_surface, self.position)

        if attack:

            ba = BossAttacks()
            ba.initializeAttack(setting, 1)
            self.all_attacks.add(ba)

    
