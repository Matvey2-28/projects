class StarSystem:
    def __init__(self, planets, name):
        self.planets = list(planets)
        self.name = name
        
    def __getitem__(self, key):
        return self.planets[key]
    
system_1 = StarSystem(['planet_1', 'planet_2'], 'System_1')
print(system_1[0])
print(system_1[0:2])