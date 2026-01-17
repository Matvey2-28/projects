def sum_arg(a, b): #Именованная функция 
    return a + b

print(sum_arg(12, 25))

sum_arg = lambda a, b: a + b #Анонимная функция

print(sum_arg(7, 13))

a_list = [lambda a, b: f'a: {b**2}' for _ in range(100)]

print(a_list[0](1, 8))

