def decorator(func):
    def wrapper():
        print(eval(func(num_1) + func(sign) + func(num_2)))
        return wrapper
    return decorator

@decorator 
def calculator(num_1, num_2, sign):
    return num_1, num_2, sign

calculator(8, 9, '+')