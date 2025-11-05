import numpy as np

from test1 import g

v0 = int(input('Введите начальную скорость: '))
x = int(input('Введите начальную координату х: '))
y = int(input('Введите начальную координату у: '))
N = 10

t = np.linspace(0, 5, N)
x1 = x + v0 * t
y1 = y + v0 * t - (g * t ** 2) / 2

output = np.zeros((N, 3))
output[:, 0] = t
output[:, 1] = x1
output[:, 2] = y1

print(output)
