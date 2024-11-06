from abstract.setting import Setting
import pygame

class PumpkinPatch(Setting):

    def __init__(self):

        self.screen = pygame.display.set_mode((800,600))
        self.screen.fill((0,0,0))
        pygame.draw.line(self.screen, (255,255,255), (0,500), (800,500))

    def getSetting(self):

        return self.screen
    
    