import numpy as np

a = [[3, 4, 1, 8, 7, 9],
     [5, 2, 1, 7, 8, 3],
     [6, 2, 1, 3, 4, 5],
     [8, 9, 0, 1, 5, 6],
     [1, 2, 3, 7, 7, 6]]

b = np.array(a)
slice1 = b[0, :3:1]
print(slice1)

slice2 = b[:3:1, 4]
print(slice2)

slice3 = b[1:3:, :2:]
print(slice3)

slice4 = b[1, 2::]
print(slice4)

slice5 = b[2::, 1:3:]
print(slice5)

slice6 = b[2::, 3:4:]
print(slice6)

slice7 = b[3::, 4::]
print(slice7)