from MattsBossLevelPart.Levels.abstract.holiday_level import HolidayLevel
from MattsBossLevelPart.Levels.settings.turkey_trail import TurkeyTrail
from MattsBossLevelPart.Levels.player.main_player import MainPlayer
from MattsBossLevelPart.Levels.bosses.thanksgivingBoss.terror_the_turkey import TerrorTheTurkey

class Thanksgiving(HolidayLevel):

    def __init__(self):

        self.tt_obj = TurkeyTrail()

    def createBoss(self):
        boss_obj = TerrorTheTurkey()

        return boss_obj

    def createPlayer(self, score):
        player_obj = MainPlayer(score)

        return player_obj

    def createSetting(self):

         thanksgivingSetting = self.tt_obj.getSetting()

         return thanksgivingSetting