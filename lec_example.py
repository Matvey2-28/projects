try:
    x = int(input('Введите первое число: '))
    y = int(input('Введите второе число: '))
    
    if x < 0 or y < 0:
        raise ValueError('Числа должны быть положительными')
        
    result = x / y
    
    print('Результат', result)
    
except ValueError as e:
    print('Ошибка:', e)
    
except ZeroDivisionError:
    print('Ошибка: деление на ноль')
    
except Exception as e:
    print('Произошла непредвиденная ошибка', e)
    
print('hello')