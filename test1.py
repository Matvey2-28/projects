import numpy as np

w = int(input('Введите start: '))
z = int(input('Введите stop: '))
g = int(input('Введите элементы массива: '))

a = np.linspace(w, z, g)

def middle(a):
    x = sum(a) / g
    print(x)
        
middle(a)
    