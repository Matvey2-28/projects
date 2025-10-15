a=range(0,10,2)
print(a)
print(type(a))
print(a[3])

a='Good'
for i in range(0,10,1):
    if i<len(a):
        print(a[i]+' - Bad')
    else:
        print(f'{i}'+' - Good')
        
for i in a:
    print(i)
    
for i in range(len(a)):
    print(i,a[i])
    
from lec_if import b 
print(b)