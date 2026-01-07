class Ball:
    
    def __init__(self):
          self.name = 'Oval' # публичная переменная
          self._radius = 5 # приватная переменная
          self.__color = 'red' # защищенная переменная
        
        
    # Публичный метод
    def update_name(self, name):
        self.name = name
        print('name update to:' + self.name)
        
    # Приватный метод
    def _update_radius(self, radius):
        self._radius = radius
        print('radius update to: ', self._radius)
        
    # Защищенный метод
    def __update_color(self, color):
        self.__color = color
        print('color update to:', self.__color)
        
    def default_color(self):
        print('default color')
        self.__update_color('red')
        
        
        
        
ball = Ball()

print(ball.name)
print(ball._radius)
# print(ball.__color)

print()
ball.update_name("Happy Oval")
ball._update_radius(5)
# ball.__update_color('blue')
ball.default_color()

ball._Ball__update_color('blue')