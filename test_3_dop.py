import matplotlib.pyplot as plt
import numpy as np

def function(a, b):
    
    x = np.arange(-100, 100, 0.01)
    if x < a:
        return a**2
    elif a <= x <= b:
        return x**2
    elif x > b:
        return b**2
    y = a * x**2 + b * x
    
    plt.plot(x, y)
    plt.savefig('test_2_dop.png')
    
if __name__ == '__main__':
    function(1, 2)