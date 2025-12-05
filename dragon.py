import time
from hero import Hero


class Dragon:

    def __init__(self, dragon_name):
        self.dragon_name = dragon_name
        self.dragon_hp = 5000
        self.dragon_dm = 100
        self.hl = 300
    
    def heal(self):
        self.hero1_hp = 0
        if hero.hero_hp < 15000:
            while hero.hero_hp < 15000:
                time.sleep(1)
                hero.hero_hp += self.hl
                self.hero1_hp = hero.hero_hp
                print(f'Герой восстанавливает здоровье: {hero.hero_hp} + {self.hl}')
                if hero.hero_hp >= 15000:
                    print(f'Герой восстановил здоровье: {self.hero1_hp}')
                    break
                    
        elif hero.hero_hp == 15000:
            print('Герой не нуждается в лечении')
            
            
            
            

hero = Hero('Makanchik')
