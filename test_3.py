import time

timer = time.time()
M = int(input('Введите переменную М: '))
N = int(input('Введите переменную N: '))

for i in range(0, M):
    for j in range(0, N):
        time.sleep(1)
        print('i = ',i)
        time.sleep(1)
        print('j = ',j)
        
print(timer)