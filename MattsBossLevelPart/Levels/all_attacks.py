from bosses.fear_the_pumpkin import FearThePumpkin
from bosses.boss_attacks import BossAttacks
import pygame

class AllAttacks:

    def __init__(self):
          
        self.sprite_group = pygame.sprite.Group()
        self.sprite_list= []

    def updateAll(self, setting, boss, player_pos):

        self.sprite_list = boss.getBossAttacks()

        self.sprite_group.add(*self.sprite_list)

        boss.clearAttackList()
        # self.sprite_set = set()

        if len(self.sprite_group)> 0:

            (px,py) = player_pos

            for sprite in self.sprite_group:

                x,y = sprite.getAttackPosition()

                if (x <= px+40) and (x>=px+25):

                    if y >= 400:

                        sprite.endAttack(setting)
                        self.sprite_group.remove(sprite)
                        del sprite

            
            self.sprite_group.update(setting)