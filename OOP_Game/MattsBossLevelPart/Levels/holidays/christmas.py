from MattsBossLevelPart.Levels.abstract.holiday_level import HolidayLevel
from MattsBossLevelPart.Levels.settings.snowmans_snowdrift import SnowmansSnowdrift
from MattsBossLevelPart.Levels.player.main_player import MainPlayer
from MattsBossLevelPart.Levels.bosses.christmasBoss.sinister_snowman import SinisterSnowman

class Christmas(HolidayLevel):

    def __init__(self, game):

        self.ss_obj = game
        self.ss_obj.screen.fill((0,0,0))

    def createBoss(self):
        boss_obj = SinisterSnowman()

        return boss_obj

    def createPlayer(self, score):
        player_obj = MainPlayer(score)

        return player_obj

    def createSetting(self):

         christmasSetting = self.ss_obj.getSetting()

         return christmasSetting