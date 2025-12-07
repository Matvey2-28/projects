import time
import random as rd
from npc import NPC 
from dragon import Dragon
from skeleton import Skeleton

class Hero:
                    
    def __init__(self, name):
        self.name = name
        self.hero_hp = 14000
                   
                           
    def attack_with_dragon(self):
        self.kills_count_with_dragon = 0
        self.deaths_count_with_dragon = 0
        while npc.npc_hp > 0:
            time.sleep(1)
            npc.npc_hp -= rd.randrange(100, 500, 50) + dragon1.dragon_dm
            print(f'Здоровье врага: {npc.npc_hp} - {rd.randrange(100, 500, 50) + dragon1.dragon_dm}')
                
            if npc.npc_hp <= 0:
                self.kills_count_with_dragon += 1
                print('Твой герой одержал победу!')
                break
                
                    
                    
    def attack_with_skeleton(self):
        self.kills_count_with_skelet = 0
        self.deaths_count_with_skelet = 0
        while npc.npc_hp > 0:
            time.sleep(1)
            npc.npc_hp -= rd.randrange(100, 500, 50) + skelet1.skelet_dm
            print(f'Здоровье врага: {npc.npc_hp} - {rd.randrange(100, 500, 50) + skelet1.skelet_dm}')
            
            if npc.npc_hp <= 0:
                self.kills_count_with_skelet += 1
                print('Твой герой одержал победу!')
                break
                
                
    def healing(self):
        self.hero1_hp = 0
        if self.hero_hp < 15000:
            while self.hero_hp < 15000:
                time.sleep(1)
                self.hero_hp += dragon1.hl
                self.hero1_hp = self.hero_hp
                print(f'Герой восстанавливает здоровье: {self.hero_hp} + {dragon1.hl}')
                if self.hero_hp >= 15000:
                    print(f'Герой восстановил здоровье: {self.hero1_hp}')
                    break
                                
                elif self.hero_hp == 15000:
                    print('Герой не нуждается в лечении')
                
                
    def go_outside(self):
        print('Ты снаружи')
        
        
    def go_in_castle(self):
        print('Ты в замке')
        
        
    def check_hero_statistics(self):
        print('________Статистика Героя________')
        print('Hero:')
        print('\t Health: ', self.hero1_hp)
        print(f'\t Monsters: {dragon1.dragon_name}, {skelet1.skelet_name}')
        print('\t Kills: ', hero.kills_count_with_dragon + hero.kills_count_with_skelet)
        print('\t Deaths: ', hero.deaths_count_with_dragon + hero.deaths_count_with_skelet)
        print('________________________________')
                    
                  

npc =  NPC('Hog Rider')
# hero = Hero('Makanchik')
dragon1 = Dragon('Leviathan')
skelet1 = Skeleton('Varior')






