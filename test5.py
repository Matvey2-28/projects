import numpy as np


def area(figure: str, *arg):
    '''
    figure: \n
    \t circle: R \n
    \t rectangle: a, b \n
    \t triangle: a, h \n
    '''
    if figure == 'circle':
        area_culc = np.pi * arg[0] ** 2
    elif figure == 'rectangle':
        area_culc = arg[0] * arg[1]
    else:
        area_culc = 0.5 * arg[0] * arg[1]
    print(area_culc)
    
    
area('circle', 7)
help(area)