from abstract.boss import Boss
import pygame

class FearThePumpkin(Boss):

    def __init__(self):

        self.position = (750,475)

    def getPosition(self):

        return self.screen
    
    def setPosition(self):

        pass

    def drawBoss(self, setting):

        pygame.draw.circle(setting, (255,255,255), self.position, 25.0) 