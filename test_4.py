import random as rd

class Planet:
    orbit = 0
    count_of_detach = 0
    def __init__(self):
        Planet.count_of_detach = Planet.count_of_detach + 1
    
    @staticmethod 
    def bomb_planet():
        print('Меня взорвали')
        
    @classmethod 
    def detach_of_orbit(cls):
        print(f'Меня сместили с орбиты на {cls.orbit - rd.randrange(100, 1000, 100)} и {cls.count_of_detach} раз')
        
    @property 
    def is_alive(self):
        print('Я жива')
        
Planet.bomb_planet()
Planet.detach_of_orbit()
pl1 = Planet()
pl2 = Planet()
pl3 = Planet()
pl4 = Planet()
pl5 = Planet()
pl6 = Planet()
Planet.detach_of_orbit()
pl1.is_alive