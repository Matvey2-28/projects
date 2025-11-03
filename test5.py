import numpy as np

N = int(input('Введите значение N: '))
M = int(input('Введите значение М: '))

trigonometry_array = np.ndarray((N, M))

for i in range(N):
    for j in range(M):
        if trigonometry_array[i, j] < 0:
            trigonometry_array[i, j] = 0            
            trigonometry_array[i, j] = np.sin(N * i + M * j + 1)            
            slice1 = trigonometry_array[0::, 0::]
            slice2 = trigonometry_array[0::, 1::]
            slice3 = trigonometry_array[0::, 2::]
            slice4 = trigonometry_array[0::, 3::]

print(slice2 + slice1 + slice3 + slice4)