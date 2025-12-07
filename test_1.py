import matplotlib.pyplot as plt
import numpy as np

def cicloid(R=5):
    
    t = np.arange(-2 * R, 2 * R, 0.1)
    
    x = R * (t - np.sin(t))
    y = R * (1 - np.cos(t))
    
    plt.plot(x, y)
    plt.savefig('cicloid.png')
    plt.close()
    
def astroid(R=5):
    
    t = np.arange(-2 * (R / 4), 2 * R, 0.1)
    
    x = R * np.cos(t) ** 3
    y = R * np.sin(t) ** 3
    
    plt.plot(x, y)
    plt.savefig('astroid.png')
    plt.close()
    
if __name__ == '__main__':
    cicloid()
    astroid()