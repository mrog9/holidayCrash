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
        self.float_x = 50.0
        
    def getPosition(self):

        quad = self.pos_x // 150

        return quad

        

    def updatePosition(self, move, right):

        if move:
           
            if right and self.pos_x < 650:
                self.vel = 0.2
            elif not right and self.pos_x > 50:
                self.vel = -0.2

            self.float_x += self.vel
            self.pos_x = math.floor(self.float_x)
            self.vel=0

        else:

            self.float_x = float(self.pos_x)
            self.vel = 0
        

    def drawPlayer(self, setting):

        pygame.draw.circle(self.surface, (255,255,255), (50,75), 25)
        setting.blit(self.surface, (self.pos_x - 50, self.pos_y  - 75))

    
         