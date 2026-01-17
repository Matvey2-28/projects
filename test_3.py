import numpy as np

class ClassVector:
    def __init__(self, vectors, x, y, z):
        self.vectors = list(vectors)
        self.x = x
        self.y = y
        self.z = z
        
    def __len__(self):
        return len(self.vectors)
    
    def __str__(self):
        return print(ClassVector())
    
    def __add__(self, other):
        i = int(input('Выберите порядковый номер обьекта: '))
        vector = self.vectors[i]
        vectors_1 = vector.append(other)
        return vectors_1
    
    def __sub__(self, other):
        i = int(input('Выберите порядковый номер обьекта: '))
        vector = self.vectors[i]
        vectors_1 = vector.remove(other)
        return vectors_1
    
    def __mul__(self, other):
        if self.other is str:
            print('Это строковая величина, нельзя перемножить')
        elif self.other is int:
            return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)) * other
    
    def __radd__(self, other):
        i = int(input('Выберите порядковый номер обьекта: '))
        vector = self.vectors[i]
        vectors_1 = vector.insert(0, other)
        return vectors_1
    
    def __rsub__(self, other):
        i = int(input('Выберите порядковый номер обьекта: '))
        vector = self.vectors[i]
        vectors_1 = vector.remove(other)
        return vectors_1
    
    def __rmul__(self, other):
        return ClassVector(other * np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2))
    
    def __iadd__(self, other):
        i = int(input('Выберите порядковый номер обьекта: '))
        vector = self.vectors[i]
        vectors_1 = vector.append(other)
        return vectors_1
    
    def __isub__(self, other):
        i = int(input('Выберите порядковый номер обьекта: '))
        vector = self.vectors[i]
        vectors_1 = vector.remove(other)
        return vectors_1
    
    def __imul__(self, other):
        return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)) * other
    
    def __eq__(self, other):
        
