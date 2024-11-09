import pygame
import random
import math

class BossAttacks(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.surface = pygame.Surface((15, 100), pygame.SRCALPHA)
        self.surface.fill((0,0,0))
        self.pos = (0,0)
        self.x = 650
        self.floatX = 650.0
        self.y = 399
        self.floatY = 399.0
        self.velX = -0.2
        self.velY = -0.002
        self.accel = 0.00002

    def initializeAttack(self,setting, pred_quad):

        pos_x = 7
        
        rand_num = random.randint(0,19)

        pos_y = pred_quad*20 + rand_num

        self.pos = (pos_x, pos_y)

        pygame.draw.circle(self.surface, (255,255,255), self.pos, 5)
        setting.blit(self.surface, (self.x, self.y))

    def update(self,setting):

        self.floatX += self.velX
        self.floatY += self.velY
        self.x = math.floor(self.floatX)
        self.y = math.floor(self.floatY)


        self.velY += self.accel

        pygame.draw.circle(self.surface, (255,255,255), self.pos, 5)
        setting.blit(self.surface, (self.x, self.y))

    def endAttack(self, setting):

        pygame.draw.circle(self.surface, (0,0,0), self.pos, 5)
        setting.blit(self.surface, (self.x, self.y))


    def getAttackPosition(self):

        return self.x, self.y