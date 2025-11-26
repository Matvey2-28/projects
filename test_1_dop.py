import time

N = 10**7

def math_func(x):
    return 4 * x ** 4 + 4 * x ** 3 - 2 * x ** 2 + 5 * x - 1

map_list = [0 for _ in range(N)]

timer = time.time()
map_list = list(map(math_func, map_list))
print(time.time() - timer)

timer = time.time()
list_comp = [math_func(x) for x in range(N)]
print(time.time() - timer)

circle_list = []
timer = time.time()
for x in range(N):
    circle_list.append(math_func(x))
print(time.time() - timer)