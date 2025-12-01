import matplotlib.pyplot as plt
import numpy as np

def krivye(t, B, b, A = 1, s = np.pi / 2, a = 1):
    if ((b / a) % 1 == 0 and (b / a) % 1 > 0) or ((a / b) % 1 == 0 and (a / b) % 1 > 0):
        global x
        global y
        x = A * np.sin(a * t + s)
        y = B * np.sin(b * t)     
        
        
    elif ((b / a) % 1 != 0) or ((a / b) % 1 != 0):
        print('Выражение недействительно')
              
plt.plot(x, y)        
plt.savefig('krivye.png')

if __name__ == '__main__':
    krivye(5, 4, 1)