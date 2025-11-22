import time
from dragon import Dragon         
from skeleton import Skeleton
        

class Hero:
                    
    def __init__(self, name: str, hero_hp: int, hero_dm: int):
        self.name = name
        self.hero_hp = hero_hp
        self.hero_dm = hero_dm
                        
    def apply_dragon(self):
        self.dragon = Dragon()
        
                        
    def apply_skeleton(self):
        self.skeleton = Skeleton()
            
                           
    def attack(self):
        if hero.apply_dragon():
            while self.hero1_hp + self.dragon_hp != 0:
                time.sleep(1)
                hero1_hp + dragon_hp -= hero_dm + dragon_dm
                print('Урон: ', hero_dm + dragon_dm)
                hero_hp + dragon_hp -= hero1_dm + dragon_dm       
                
                if self.hero1_hp + self.dragon_hp <= 0:
                    break
                    print('Твой герой одержал победу!')
                    
        elif hero.apply_skeleton():
            while self.hero1_hp + self.skelet_hp != 0:
                time.sleep(1)
                hero1_hp + skelet_hp -= hero_dm + skelet_dm
                print('Урон: ', hero_dm + skelet_dm)
                hero_hp + skelet_hp -= hero1_dm + skelet_dm  

                if self.hero1_hp + self.skelet_hp <= 0:
                    break
                    print('Твой герой одержал победу!')
                elif self.hero_hp + self.skelet_hp <= 0:
                    break
                    print('Твой герой проиграл!')
                    
                        
                    
hero = Hero()                   
                    
                 
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
  