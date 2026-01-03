import time


def timer(func):
    def function():
        timer = time.time()
        func()
        print(time.time() - timer)
    return function

@timer 
def func_1():
    print('Функция начала свою работу')
    for i in range(10):
        time.sleep(1)
        print('Функция работает')
    print('Функция завершила свою работу')

func_1()