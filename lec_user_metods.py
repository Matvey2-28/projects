class Ball:
    
    def __init__(self,mass):
        
        self.mass=mass
        self.image='hexagone'
        self.x=0
        self.y=0
    def drop(self):
        print('я подбросился')
        self.y=2
        
    def kick(self):
        print('я пнулся')
        self.x += 1
        
    def fail(self):
        self.mass=self.mass-0.1
        
ball=Ball(0.5)
ball.drop()
ball.kick()
ball.fail()
print(ball.x)
print(ball.mass)
ball.kick()
ball.kick()
ball.kick()
ball.kick()
ball.kick()
ball.kick()
ball.kick()
print(ball.x)