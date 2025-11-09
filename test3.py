g = 9.8
m = int(input('Введите массу тела: '))
v = int(input('Введите скорость тела: '))
h = int(input('Введите высоту: '))

def energy(g, m, v, h):
    E = m * g * h + m * v ** 2 / 2
    print(E)
    
energy(g, m, v, h)