class StarSystem:
    def __init__(self, planets, name):
        self.planets = list(planets)
        self.name = name
        
    def __bool__(self):
        return len(self.planets) > 0
    
system_1 = StarSystem(['planet_1', 'planet_2'], 'System_1')
system_2 = StarSystem([], 'System_2')

print(bool(system_1))
print(bool(system_2))