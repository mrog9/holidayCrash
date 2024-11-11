from abstract.boss import Boss
import pygame
import torch
from .boss_attacks import BossAttacks

class FearThePumpkin(Boss):

    def __init__(self):

        self.position = (675,399)
        self.boss_surface = pygame.Surface((100,100))
        self.all_attacks = []
        self.p_surface = pygame.Surface((250, 30))
        self.p_surface.fill((255,165,0))
        self.image = pygame.image.load("MattsBossLevelPart/Levels/bosses/pumpkin.png")
        self.scaled_img = pygame.transform.scale(self.image, (80,80))
        self.damage = 0



    def getPosition(self):

        return self.position
    
    def setPosition(self):

        pass

    def drawBoss(self, setting, attack):

        
        # pygame.draw.circle(self.boss_surface, (255,255,255), (50,75), 25)
        self.boss_surface.blit(self.scaled_img, (10,20))
        setting.blit(self.boss_surface, self.position)

        setting.blit(self.p_surface, (525,25))
        damage = pygame.Surface((self.damage, 30))
        damage.fill((0,0,0))
        setting.blit(damage,(775 - self.damage, 25))

        if attack:

            ba = BossAttacks()
            ba.initializeAttack(setting, 1)
            self.all_attacks.append(ba)

    def reduceHealth(self):

        self.damage += 50

        if self.damage < 250:

            return True
        
        else:

            return False

    def getBossAttacks(self):

        return self.all_attacks
    
    def clearAttackList(self):

        self.all_attacks = []



    
