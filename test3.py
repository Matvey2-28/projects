import numpy as np

from test1 import g

v0 = int(input('Введите начальную скорость: '))
x = int(input('Введите начальную координату х: '))
y = int(input('Введите начальную координату у: '))



print('t x y')

for t in range(0,6):
    for x1 in range(0,6):
        for y1 in range(0,6):
            x1 = x + v0 * t
            y1 = y + v0 * t - (g * t ** 2) / 2
            print(t, x1, y1)
