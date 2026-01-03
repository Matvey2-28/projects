def decorator(func):
    print('Hello world')
    return func

@decorator   
def decorate_example():
    print('Здарова йоу')
    
decorate_example()


# Другое обьявление декоратора
decorate_example = decorator(decorate_example)
decorate_example()