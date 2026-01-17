def solar_sys_generate():
    
    for i in ['mercury', 'venus', 'earth']:
        yield i
        
planets = solar_sys_generate()
iter_planets = iter(planets)
print(type(iter_planets))
print(next(iter_planets))
print(next(iter_planets))
print(next(iter_planets))