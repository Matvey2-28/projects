a = int(input('Введите первое число: '))

b = int(input('Введите второе число: '))
if b==0:
    print('На ноль не делят')
    
elif a%b==0:
    print('Делится')
    print(a%b)
    
else:
    print('Не делится')
    print(a/b)
        

    