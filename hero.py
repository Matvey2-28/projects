# import time
# from npc import NPC 
# from dragon import Dragon
# from skeleton import Skeleton

class Hero:
                    
    def __init__(self, name):
        self.name = name
        self.hero_hp = 14000
        self.hero_dm = 300
                   
                           
    def attack_with_dragon(self):
        self.kills_count_with_dragon = 0
        self.deaths_count_with_dragon = 0
        while npc.npc_hp > 0:
            time.sleep(1)
            npc.npc_hp -= self.hero_dm + dragon1.dragon_dm
            print(f'Здоровье врага: {npc.npc_hp} - {self.hero_dm + dragon1.dragon_dm}')
                
            if npc.npc_hp <= 0:
                self.kills_count_with_dragon += 1
                print('Твой герой одержал победу!')
                break
                
                    
                    
    def attack_with_skeleton(self):
        self.kills_count_with_skelet = 0
        self.deaths_count_with_skelet = 0
        while npc.npc_hp > 0:
            time.sleep(1)
            npc.npc_hp -= self.hero_dm + skelet1.skelet_dm
            print(f'Здоровье врага: {npc.npc_hp} - {self.hero_dm + skelet1.skelet_dm}')
            
            if npc.npc_hp <= 0:
                self.kills_count_with_skelet += 1
                print('Твой герой одержал победу!')
                break
                
                
                
    def go_outside(self):
        print('Ты снаружи')
        
        
    def go_in_castle(self):
        print('Ты в замке')
        
        
    def check_hero_statistics(self):
        print('________Статистика Героя________')
        print('Hero:')
        print('\t Health: ', dragon1.hero1_hp)
        print(f'\t Monsters: {dragon1.dragon_name}, {skelet1.skelet_name}')
        print('\t Kills: ', self.kills_count_with_dragon + self.kills_count_with_skelet)
        print('\t Deaths: ', self.deaths_count_with_dragon + self.deaths_count_with_skelet)
        print('________________________________')
                    
                  

# npc =  NPC('Hog Rider')
# # hero = Hero('Makanchik')
# dragon1 = Dragon('Leviathan')
# skelet1 = Skeleton('Varior')






