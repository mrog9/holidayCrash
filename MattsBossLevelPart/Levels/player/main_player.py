from abstract.player import Player
import pygame
import math

class MainPlayer(Player):

    def __init__(self):

        self.pos_x = 50
        self.pos_y = 474
        self.vel = 0
        self.surface = pygame.Surface((100,100))
        self.surface.fill((0,0,0))
        
    def getPosition(self):

        pass

    def updatePosition(self, duration, right):

        if right:
            self.vel += math.ceil(duration)*10
        else:
            self.vel -= math.ceil(duration)*10

        self.pos_x += self.vel
        self.vel = 0
        

    def drawPlayer(self, setting):

        pygame.draw.circle(self.surface, (255,255,255), (50,75), 25)
        setting.blit(self.surface, (self.pos_x - 50, self.pos_y  - 75))

    
         