import time
from hero import *


class Dragon:

    def __init__(self, dragon_name: str, dragon_hp: int, dragon_dm: int, hl: int):
        self.dragon_name = dragon_name
        self.dragon_hp = dragon_hp
        self.dragon_dm = dragon_dm
        self.hl = hl
    
    def heal(self):
        if self.hero_hp < 1500:
            while self.hero_hp != 1500:
                time.sleep(1)
                hero_hp += hl
                print('Герой восстанавливает здоровье: ', hero_hp)
                if self.hero_hp == 1500:
                    break
                    print('Герой восстановил здоровье')
        elif self.hero_hp == 1500:
            print('Герой не нуждается в лечении')
            
            
            
            
            

