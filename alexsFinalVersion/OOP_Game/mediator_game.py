from alexsGame import Game
import pygame
import sys
from MattsBossLevelPart.Levels.runs.halloween_run import runHalloween
from MattsBossLevelPart.Levels.runs.thanksgiving_run import runThanksgiving
from MattsBossLevelPart.Levels.runs.christmans_run import runChristmas
from sprites import Spritesheet

class Mediator:

    def __init__(self):

        self.playing=True
        self.score = 0

    def getPlayingStatus(self):

        return self.playing
        
    def run1(self):

        g = Game(self.score)
        g.intro_screen()
        g.set_ss(
            Spritesheet('alexsFinalVersion/OOP_Game/img/Halloween_Wall_Sheet.png', 4, 4, 32, [4,4,4,4], 0),
			Spritesheet('alexsFinalVersion/OOP_Game/img/Halloween_Enemy_Sheet.png', 6, 5, 32, [4, 3, 4, 4, 5, 5, 5], 4)
        )
        g.new()
        self.score = g.main()

        if g.winning == False:
            g.game_over()
            self.playing = False

        pygame.quit()

        if self.playing:
            self.score = runHalloween(self.score)


    def run2(self):
        pygame.init()
        g = Game(self.score)
        
        g.set_ss(
            Spritesheet('alexsFinalVersion/OOP_Game/img/Thanksgiving_Wall_Sheet.png', 4, 4, 32, [4,4,4,4], 0),
			Spritesheet('alexsFinalVersion/OOP_Game/img/Thanksgiving_Enemy_Sheet.png', 6, 5, 32, [4, 3, 4, 4, 5, 5, 5], 4)
        )
        
        g.new()

        self.score = g.main()

        pygame.quit()

        if self.playing:

            self.score = runThanksgiving(self.score)

    def run3(self):

        pygame.init()

        g = Game(self.score)

        g.set_ss(
            Spritesheet('alexsFinalVersion/OOP_Game/img/Christmas_Wall_Sheet.png', 4, 4, 32, [4,4,4,4], 0),
			Spritesheet('alexsFinalVersion/OOP_Game/img/Christmas_Enemy_Sheet.png', 6, 5, 32, [4, 4, 5, 5, 4, 4, 4], 4)
        )

        g.new()

        self.score = g.main()

        pygame.quit()

        if self.playing:

            self.score = runChristmas(self.score)
