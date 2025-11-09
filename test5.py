import numpy as np

def area_trangle(a, h):
    trangle = a * h / 2
    print(trangle)
    
def area_square(a):
    square = a ** 2
    print(square)

def  area_circle(r):  
    circle = np.pi * r ** 2
    print(circle)

area_trangle(2, 3)
area_square(4)
area_circle(2)