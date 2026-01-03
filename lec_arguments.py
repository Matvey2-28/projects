def decorator(func):
    def wrapped_function(str):
        func(str)
    return wrapped_function


@decorator  
def greet(name):
    print(f'Привет, {name}')
    
greet('Анастасия')