import numpy as np

z = int(input('Введите start: '))
y = int(input('Введите stop: '))
w = int(input('Введите элементы массива: '))

a = np.linspace(z, y, w)

def function(a):
    x = np.prod(a)
    print(x)
    
function(a)