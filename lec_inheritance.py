import numpy as np

class Ball:
    
    def __init__(self, end_time, color):
        self.color = color
        self.time = np.arange(0, end_time, 0.1)
        
        
    def move_ball(self, vx, vy):
        self.x = vx * self.time
        self.y = vy * self.time
        print(f'Координаты объекта \n (x: {self.x}, \n y: {self.y})')
        
class FootBall(Ball):
    
    def __init__(self, aerodinamics, color):
        super().__init__(end_time=5, color=color)
        self.aerodinamics = aerodinamics
        
    def fly(self):
        if self.aerodinamics == 'circle':
            print('True fly')
        else:
            print('Not play')
            
            
            
            
ball = FootBall(aerodinamics='circle', color='red')
ball.fly()
ball.move_ball(4, 5)