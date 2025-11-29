import time
from dragon import *         
from skeleton import *
from npc import *
        

class Hero:
                    
    def __init__(self, name: str, hero_hp: int, hero_dm: int):
        self.name = name
        self.hero_hp = hero_hp
        self.hero_dm = hero_dm
                   
                           
    def attack_with_dragon(self):
        while npc.self.npc_hp != 0:
            time.sleep(1)
            npc_hp -= hero_dm + dragon_dm
            print('Урон: ', hero_dm + dragon_dm)
                
            if self.npc_hp <= 0:
                break
                print('Твой герой одержал победу!')
                    
                    
    def attack_with_skeleton(self):
        while npc.self.npc_hp != 0:
            time.sleep(1)
            npc_hp -= hero_dm + skelet_dm
            print('Урон: ', hero_dm + skelet_dm)
            if self.npc_hp <= 0:
                break
                print('Твой герой одержал победу!')
                    
                  

npc =  NPC('Hog Rider', 1500, 60)
hero = Hero('Makanchik', 1500, 100)
dragon1 = Dragon('Leviathan', 500, 50, 50)
skelet1 = Skeleton('Varior', 700, 70)