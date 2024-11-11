import pygame
import random
import math

class PlayerAttacks(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.surface = pygame.Surface((15, 100), pygame.SRCALPHA)
        self.surface.fill((0,0,0))
        self.pos = (9,6)
        self.x = 105
        self.floatX = 105.0
        self.y = 440
        self.floatY = 440.0
        self.velX = 0.2
        self.velY = 0
        self.accel = 0.00002
        self.pow = 0

    def initializeAttack(self,setting,power):

        self.pow = power
        pygame.draw.circle(self.surface, (200,200,200), self.pos, 5)
        setting.blit(self.surface, (self.x, self.y))

    def update(self,setting):

        self.floatX += self.velX
        self.floatY += self.pow
        self.x = math.floor(self.floatX)
        self.y = math.floor(self.floatY)


        self.velY += self.accel

        pygame.draw.circle(self.surface, (200,200,200), self.pos, 5)
        setting.blit(self.surface, (self.x, self.y))

    def endAttack(self, setting):

        pygame.draw.circle(self.surface, (0,0,0), self.pos, 5)
        setting.blit(self.surface, (self.x, self.y))


    def getAttackPosition(self):

        return self.x, self.y