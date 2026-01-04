def first_num(num_1):
    def decorator(func):
        def wrapper(num_2):
            print(num_1 + func(num_2))
        return wrapper 
    return decorator

@first_num(5)
def second_num(num_2):
    return num_2

second_num(3)