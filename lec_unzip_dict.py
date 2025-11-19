def parameters(**kwargs):
    print(kwargs)
    
parameters(first=1, second='two', something=False)


def discriminant(a, b, c):
    return b * b - 4 * a * c

polynom = {'a': 1, 'b': 0, 'c': 2}

print(discriminant(**polynom))