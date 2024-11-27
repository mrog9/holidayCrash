from MattsBossLevelPart.Levels.abstract.holiday_level import HolidayLevel
from MattsBossLevelPart.Levels.settings.pumpkin_patch import PumpkinPatch
from MattsBossLevelPart.Levels.player.main_player import MainPlayer
from MattsBossLevelPart.Levels.bosses.halloweenBoss.fear_the_pumpkin import FearThePumpkin
import config

class Halloween(HolidayLevel):

    def __init__(self, game):

        self.pp_obj = game
        self.pp_obj.screen.fill((0,0,0))

    def createBoss(self):
        boss_obj = FearThePumpkin()

        return boss_obj

    def createPlayer(self, score):
        player_obj = MainPlayer(score)

        return player_obj

    def createSetting(self):

         halloweenSetting = self.pp_obj.getSetting()

         return halloweenSetting
         