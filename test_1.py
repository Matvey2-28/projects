class StarSystem:
    def __init__(self, planets, name):
        self.planets = list(planets)
        self.name = name
        
    def __sub__(self, other):
        planets_1 = self.planets
        planets_1.remove(other)
        return StarSystem(planets_1, self.name)
      
    def __rsub__(self, other):
        planets_1 = self.planets
        planets_1.insert(0, other)
        return StarSystem(planets_1, self.name)
    
    def __isub__(self, other):
        planets_1 = self.planets
        self.planets.remove(other)
        return StarSystem(planets_1, self.name)
        
      
system_1 = StarSystem(['planet_1', 'planet_2'], 'System_1')
system_1 = system_1 - 'planet_2'
print(system_1.planets)

system_1 = 'planet_2' - system_1
print(system_1.planets)

system_1 -= 'planet_2'
print(system_1.planets)