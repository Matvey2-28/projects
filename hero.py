import time
import random as rd

class Hero:
                    
    def __init__(self, name):
        self.name = name
        self.hero_hp = 14000
        self.hero1_hp = 14000 
        self.kills_count_with_dragon = 0
        self.deaths_count_with_dragon = 0
        self.kills_count_with_skelet = 0
        self.deaths_count_with_skelet = 0
                   
                           
    def attack_with_dragon(self, npc, dragon):
      
        while npc.npc_hp > 0:
            time.sleep(1)
            damage = rd.randrange(100, 500, 50) + dragon.dragon_dm
            npc.npc_hp -= damage
            print(f'Здоровье врага: {npc.npc_hp + damage} - {damage} = {npc.npc_hp}')
                
            if npc.npc_hp <= 0:
                self.kills_count_with_dragon += 1
                print('Твой герой одержал победу!')
                break
                
                    
                    
    def attack_with_skeleton(self, npc, skeleton):
     
        while npc.npc_hp > 0:
            time.sleep(1)
            damage = rd.randrange(100, 500, 50) + skeleton.skelet_dm
            npc.npc_hp -= damage
            print(f'Здоровье врага: {npc.npc_hp + damage} - {damage} = {npc.npc_hp}')
            
            if npc.npc_hp <= 0:
                self.kills_count_with_skelet += 1
                print('Твой герой одержал победу!')
                break
                
                
    def healing(self, dragon):

        if self.hero_hp < 15000:
            while self.hero_hp < 15000:
                time.sleep(1)
                self.hero_hp += dragon.hl
                self.hero1_hp = self.hero_hp
                print(f'Герой восстанавливает здоровье: {self.hero_hp - dragon.hl} + {dragon.hl} = {self.hero_hp}')
                
                if self.hero_hp >= 15000:
                    
                   if self.hero_hp > 15000:
                        self.hero_hp = 15000
                        self.hero1_hp = 15000
                        print(f'Герой восстановил здоровье: {self.hero1_hp}')
                        break
                                
                elif self.hero_hp == 15000 or self.hero_hp > 15000:
                    print('Герой не нуждается в лечении')
                    self.hero_hp = 15000
                    self.hero1_hp = 15000
                
                
    def go_outside(self):
        print('Ты снаружи')
        
        
    def go_in_castle(self):
        print('Ты в замке')
        
        
    def check_hero_statistics(self, dragon, skeleton):
        print('________Статистика Героя________')
        print(f'Hero: {self.name}')
        print(f'\t Health: {self.hero1_hp}')
        print(f'\t Monsters: {dragon.dragon_name}, {skeleton.skelet_name}')
        print(f'\t Kills: {self.kills_count_with_dragon + self.kills_count_with_skelet}')
        print(f'\t Deaths: {self.deaths_count_with_dragon + self.deaths_count_with_skelet}')
        print('________________________________')
                    