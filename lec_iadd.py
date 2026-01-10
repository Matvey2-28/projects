class StarSystem:
    def __init__(self, planets, name):
        self.planets = list(planets)
        self.name = name
        
    def __iadd__(self, other):
        self.planets.append(other)
        return self
      
system_1 = StarSystem(['planet_1'], 'System_1')
system_1 += 'planet_2'
print(system_1.planets)