a = int(input('Введите первое число: '))

b = int(input('Введите второе число: '))

if a>b:
    print('Делится')
    print(a%b)
    
if a<b:
    print('Не делится')
        
if b==0:
    print('На ноль не делят')
    