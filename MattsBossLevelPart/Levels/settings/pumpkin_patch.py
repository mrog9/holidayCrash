from abstract.setting import Setting
import pygame

class PumpkinPatch(Setting):

    def __init__(self):

        self.screen = pygame.display.set_mode((800,600))
        self.screen.fill((0,0,0))
        self.surface = pygame.Surface((800,100))
        self.surface.fill((255,165,0))

        pygame.init()
        pygame.mixer.music.load('MattsBossLevelPart/Levels/settings/lofiMusic.mp3')
        pygame.mixer.music.play(-1)

    def getSetting(self):

        self.screen.blit(self.surface, (0,500))

        return self.screen
    
    