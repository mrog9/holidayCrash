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
        self.p_surface = pygame.Surface((250, 30))
        self.p_surface.fill((0,0,0))
        self.image = pygame.image.load("MattsBossLevelPart/Levels/player/owl.png")
        self.scaled_img = pygame.transform.scale(self.image, (60,60))
        
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

        self.surface.blit(self.scaled_img, (10,1))
        setting.blit(self.surface, (self.pos_x - 26, self.pos_y  - 35))
        pygame.draw.rect(self.p_surface, (200,200,200), (0,0,250,30))
        setting.blit(self.p_surface, (25,25))

    
         