import numpy as np

def calculate_area(shape, *args):
    list_1 = list(*args)
    if shape == 'круг':
        list_1 = list_1.append(r)
        return np.pi * r ** 2
    elif shape == 'прямоугольник':
        list_1 = list_1.append(a, b)
        return a * b 
    elif shape == 'квадрат':
        list_1 = list_1.append(a) 
        return a ** 2
    elif shape == 'треугольник':
        list_1 = list_1.append(a, b)
        return a * b / 2
    else:
        try:
            raise ValueError
        except ValueError:
            print('Неправильное название фигуры')
                
            
    for arg in list_1:
        if arg < 0:
            try:
                raise ValueError
            except ValueError:
                print('Числа должны быть положительными')
            
calculate_area('квадрат', 12)