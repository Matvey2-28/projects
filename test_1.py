import numpy as np

a = [52, 67, 42]
b = [23, 12, 99]
c = [45, 74, 24]
d = np.random.uniform(0, 1, 100)

a1 = np.array(a)
b1 = np.array(b)
c1 = np.array(c)

print(max(max(a1), max(b1), max(c1)))
print(sum(a1) + sum(b1) + sum(c1))
print(d)