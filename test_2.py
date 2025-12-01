import matplotlib.pyplot as plt
import numpy as np

def hyperbola(x_limits0, x_limits1, N, a = 1, b =1):
    
    x = np.arange(x_limits0, x_limits1, N)
    y = a / x + b
    
    plt.plot(x, y, label='Hyperbola')
    plt.savefig('hyperbola.png')
    
if __name__ == '__main__':
    hyperbola(-5000, 5000, 1000)