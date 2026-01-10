class StarSystem:
    def __init__(self, planets, name):
        self.planets = list(planets)
        self.name = name
        
    def __len__(self):
        return len(self.planets)
    
    def __add__(self, other):
        planets_1 = self.planets.copy()
        planets_1.append(other)
        return StarSystem(planets_1, self.name)
    
system = StarSystem(['planet1', 'planet2', 'planet3'], 
                    'StarSystem1')
print(len(system))
system = system + 'planet4'
print(system.planets)