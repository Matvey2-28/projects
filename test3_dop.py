def picture(F, f, d):
    if d > 2 * F and (F < f and f < 2 * F):
        print('Действительное, перевернутое, уменьшенное')
        
    elif d == 2 * F and f == 2 * F:
        print('Действительное, перевернутое, того же размера')
        
    elif (F < d and d < 2 * F) and f > 2 * F:
        print('Действительное, перевернутое, увеличенное')
        
    elif d < F and f < 0:
        print('Мнимое, прямое, увеличенное')
        
picture(2, 3, 1)