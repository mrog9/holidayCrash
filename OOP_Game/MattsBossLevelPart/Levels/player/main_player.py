from MattsBossLevelPart.Levels.abstract.player import Player
from .player_attacks import PlayerAttacks
import pygame
import math

class MainPlayer(Player):

    def __init__(self, score):

        self.pos_x = 24
        self.pos_y = 440
        self.vel = 0
        self.surface = pygame.Surface((80,70))
        self.surface.fill((0,0,0))
        self.float_x = 50.0
        self.p_surface = pygame.Surface((250, 30))
        self.p_surface.fill((200,200,200))
        self.image = pygame.image.load("MattsBossLevelPart/Levels/player/owl.png")
        self.scaled_img = pygame.transform.scale(self.image, (60,60))
        self.damage = 0
        self.all_attacks=[]
        self.score = score
        
    def getPosition(self):

        pos = (self.pos_x, self.pos_y)

        return pos

        

    def updatePosition(self, move, right):

        if move:
           
            if right and self.pos_x < 650:
                self.vel = 1.0
            elif not right and self.pos_x > 50:
                self.vel = -1.0

            self.float_x += self.vel
            self.pos_x = math.floor(self.float_x)
            self.vel=0

        else:

            self.float_x = float(self.pos_x)
            self.vel = 0
        

    def drawPlayer(self, setting, attack, power):

        self.surface.blit(self.scaled_img, (10,1))
        setting.blit(self.surface, (self.pos_x, self.pos_y))
        setting.blit(self.p_surface, (25,25))
        damage = pygame.Surface((self.damage, 30))
        damage.fill((0,0,0))
        setting.blit(damage,(275 - self.damage, 25))

        if attack:

            pa = PlayerAttacks()

            pa.initializeAttack(setting, power, self.pos_x)
            self.all_attacks.append(pa)        

    def reduceHealth(self):

        self.damage += 50

        if self.damage < 250:

            return True
        
        else:

            return False
        
    def getPlayerAttacks(self):

        return self.all_attacks
    
    def clearAttackList(self):

        self.all_attacks = []