a1 = int(input('Введите первый член: '))
q = int(input('Введите знаменатель: '))
a = int(input('Введите количество членов прогрессии: '))

for i in range(a):
    a1 *= q
    print(a1)