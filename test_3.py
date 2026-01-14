import numpy as np

class ClassVector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __len__(self):
        return len(np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2))
    
    def __str__(self):
        return print(ClassVector())
    
    def __add__(self, other):
        return ClassVector(len(np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)) + other)
    
    def __sub__(self, other):
        return ClassVector(len(np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)) - other)
    
    def __mul__(self, other):
        if self.other is str:
            print('Это строковая величина, нельзя перемножить')
        elif self.other is int:
            return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)) * other
    
