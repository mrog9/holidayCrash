from abstract.player import Player
import pygame

class MainPlayer(Player):

    def __init__(self):

        self.position = (50,475)

    def getPosition(self):

        return self.screen
    
    def setPosition(self):

        pass

    def drawPlayer(self, setting):

        pygame.draw.circle(setting, (255,255,255), self.position, 25.0) 