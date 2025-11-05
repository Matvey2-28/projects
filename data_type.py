x = 3
y = 4

z = complex(x, y)
print(z)

w = complex(y, x)
print(z + w)

s = 'hello'
print(s[0])

#s[0] = 'H'

# Tuple
t = (1, 4, 5)
print(t)
print(t[0])

#t[0] = 3

# Dict
d = {'key_1': 4, 2: 'red', 'str': 'Hello'}

d['key_2'] = 5
print(d)

for keys in d.items():
    print(keys[1])