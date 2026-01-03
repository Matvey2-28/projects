def add_explosion(class_to_decorate):
    class DecoratedClass(class_to_decorate):
        def explode(self):
            print('Я взорвался')
            
    return DecoratedClass

@add_explosion 
class Planet:
    def exist(self):
        print('Я существую')
        
planet = Planet()
planet.exist()
planet.explode()