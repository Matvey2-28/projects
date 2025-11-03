import numpy as np

N = int(input('Введите значение N: '))
M = int(input('Введите значение М: '))

trigonometry_array = np.ndarray((N, M))

for i in range(N):
    for j in range(M):
        if trigonometry_array[i, j] < 0:
            trigonometry_array[i, j] = 0            
            trigonometry_array[i, j] = np.sin(N * i + M * j + 1)

print(trigonometry_array)