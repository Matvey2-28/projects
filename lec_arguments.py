def my_func(a, b):
    x = 3 * a - b
    return x

#tmp = my_func()

def my_func(a=1, b=0):
    x = 3 * a - b
    return x

print(my_func())
print(my_func(3, 4))
print(my_func(3))
print(my_func(b=3))
print(my_func(b=3, a=9))

def my_func(a, b=0):
    x = 3 * a - b
    return x

# ТАК НЕЛЬЗЯ:
# def my_func(a=0, b):
#   x = 3 * a - b

def my_func(*args):
    x = 3 * args[0] - args[1] * len(args)
    
    return x

print(my_func(1, 4 ,5, 6, 8))

def my_func(**kwrgs):
    x = 3 * kwrgs['obj_1'] - kwrgs['obj_2']
    return x

x = my_func(obj_1=2, obj_2=1, obj_3=4)
print(x)

def my_func(a, b, c=4, d=5, *args, **kwrgs):
    print(args)
    print(kwrgs)
    
my_func(7, 8, 6, 9, 6, 4, 3, g=4, j=7)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    