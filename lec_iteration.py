f = open('example.txt')
'''
example.txt example_2.txt
x           1
2 + x       1 + 1
'''
# print(f.readline(), end='')
# print(f.readline(), end='')
# print(f.readline(), end='')

print(next(f), end = '')
print(next(f), end = '')

f2 = open('example_2.txt')
for i in f2:
    print(i, end = '')

    
f.close()
f2.close()