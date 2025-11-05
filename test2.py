import numpy as np
from test1 import g, k, e, h

h = 100
a = 45
B = 35

v = np.sqrt((g * h * np.tan(B) ** 2) / (2 * np.cos(a) ** 2 * (1 - np.tan(B) * np.tan(a))))

print(v)

T = 200
E = 300

N = 2 / np.sqrt(np.pi) * (np.sqrt(h) * (k * T) ** (3 / 2)) * (e ** (E / (k * T))) * E ** (T / 2)

print(N)