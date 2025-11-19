name = 'matvey malik'
name0 = '_'.join(name)

for symbol in name0:
    print(ord(symbol), end = ', ')
print()

a = [109, 95, 97, 95, 116, 95, 118, 95, 101, 95, 121, 95, 32, 95, 109, 95, 97, 95, 108, 95, 105, 95, 107]


name1 = name.upper()
name2 = '_'.join(name1)

for symbol in name2:
    print(ord(symbol), end = ', ')
print()

b = [77, 95, 65, 95, 84, 95, 86, 95, 69, 95, 89, 95, 32, 95, 77, 95, 65, 95, 76, 95, 73, 95, 75]

print(min(min(a), min(b)))
print(max(max(a), max(b)))