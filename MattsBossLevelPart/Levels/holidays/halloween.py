from abstract.holiday_level import HolidayLevel
from settings.pumpkin_patch import PumpkinPatch
from player.main_player import MainPlayer
from bosses.fear_the_pumpkin import FearThePumpkin

class Halloween(HolidayLevel):

    def createBoss(self):
        boss_obj = FearThePumpkin()

        return boss_obj

    def createPlayer(self):
        player_obj = MainPlayer()

        return player_obj

    def createSetting(self):
         pp = PumpkinPatch()

         halloweenSetting = pp.getSetting()

         return halloweenSetting
         