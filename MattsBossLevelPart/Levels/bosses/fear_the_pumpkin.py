from abstract.boss import Boss
import pygame
import torch
from .boss_attacks import BossAttacks
from .pumpkin_nn import PumpkinNN

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
        self.nnModel =  PumpkinNN(20, 4)
        self.optim = torch.optim.Adam(self.nnModel.parameters(), 0.01)



    def getPosition(self):

        return self.position
    
    def setPosition(self):

        pass

    def drawBoss(self, setting, attack, p_pos_list):

        # pygame.draw.circle(self.boss_surface, (255,255,255), (50,75), 25)
        self.boss_surface.blit(self.scaled_img, (10,20))
        setting.blit(self.boss_surface, self.position)

        setting.blit(self.p_surface, (525,25))
        damage = pygame.Surface((self.damage, 30))
        damage.fill((0,0,0))
        setting.blit(damage,(525, 25))

        if attack:

            p_pos_tens = torch.stack(p_pos_list[0:21]).float()
            true_pos = torch.tensor([p_pos_list[-1]])
            sec_num = (true_pos +50 )// 150
            true_sec_tens = torch.tensor([sec_num]) 

            sec_probs = self.nnModel(p_pos_tens)
            self.nnModel.updateModel(sec_probs,true_sec_tens, self.optim)

            _, sec_num = torch.max(sec_probs, dim= -1)

            ba = BossAttacks()
            ba.initializeAttack(setting, sec_num)
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



    
