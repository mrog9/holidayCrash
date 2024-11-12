import pygame
import random
import math

class BossAttacks(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.surface = pygame.Surface((15, 15), pygame.SRCALPHA)
        self.surface.fill((0,0,0))
        self.pos = (9,9)
        self.x = 650
        self.floatX = 650.0
        self.y = 399
        self.floatY = 399.0
        self.velX = -0.13
        self.velY_list = [-0.22, -0.16, -0.10, -0.05]
        self.velY = 0
        self.accel = 0.0001

    def initializeAttack(self,setting, pred_sec):
        
        rand_list = [self.velY_list[pred_sec] + 0.01*i for i in range(11)]
        rand_int = random.randint(0,10)
        self.velY = rand_list[rand_int]

        pygame.draw.circle(self.surface, (255,165,0), self.pos, 5)
        setting.blit(self.surface, (self.x, self.y))

    def update(self,setting):

        self.floatX += self.velX
        self.floatY += self.velY
        self.x = math.floor(self.floatX)
        self.y = math.floor(self.floatY)


        self.velY += self.accel

        pygame.draw.circle(self.surface, (255,165,0), self.pos, 5)
        setting.blit(self.surface, (self.x, self.y))

    def endAttack(self, setting):

        pygame.draw.circle(self.surface, (0,0,0), self.pos, 5)
        setting.blit(self.surface, (self.x, self.y))


    def getAttackPosition(self):

        return self.x, self.y