from abstract.player import Player
import pygame
import math

class MainPlayer(Player):

    def __init__(self):

        self.pos_x = 50
        self.pos_y = 474
        self.vel = 0
        self.surface = pygame.Surface((60,60))
        self.surface.fill((0,0,0))
        self.float_x = 50.0
        
    def getPosition(self):

        pos = (self.pos_x, self.pos_y)

        return pos

        

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

        pygame.draw.circle(self.surface, (255,255,255), (26,35), 25)
        setting.blit(self.surface, (self.pos_x - 26, self.pos_y  - 35))

    
         