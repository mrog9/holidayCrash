from bosses.fear_the_pumpkin import FearThePumpkin
from bosses.boss_attacks import BossAttacks
from player.main_player import MainPlayer
import pygame

class AllAttacks:

    def __init__(self):
          
        self.boss_sprite_group = pygame.sprite.Group()
        self.boss_sprite_list= []
        self.player_sprite_group = pygame.sprite.Group()
        self.player_sprite_list = []

    def updateAll(self, setting, boss, player):

        self.boss_sprite_list = boss.getBossAttacks()
        self.player_sprite_list = player.getPlayerAttacks()

        self.boss_sprite_group.add(*self.boss_sprite_list)
        self.player_sprite_group.add(*self.player_sprite_list)

        boss.clearAttackList()
        player.clearAttackList()

        p_IS_alive = True
        b_IS_alive = True

        if len(self.boss_sprite_group)> 0:

            (px,py) = player.getPosition()
            

            for sprite in self.boss_sprite_group:

                x,y = sprite.getAttackPosition()

                if (x <= px+100) and (x>=px):

                    if y >= 400 and y<=450:

                        sprite.endAttack(setting)
                        self.boss_sprite_group.remove(sprite)
                        del sprite

                        p_IS_alive = player.reduceHealth()

        if len(self.player_sprite_group)> 0:

            (bx,by) = boss.getPosition()
            

            for sprite in self.player_sprite_group:

                x,y = sprite.getAttackPosition()

                if (x <= bx+100) and (x>=bx):

                    if y >= by-10 and y<=by+100:

                        sprite.endAttack(setting)
                        self.player_sprite_group.remove(sprite)
                        del sprite

                        b_IS_alive = boss.reduceHealth()


            
        self.boss_sprite_group.update(setting)
        self.player_sprite_group.update(setting)

        return p_IS_alive, b_IS_alive