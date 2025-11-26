import matplotlib.pyplot as plt
import numpy as np

def circle(radius=10):
    
    x = np.arange(-2 * radius, 2 * radius, 0.1)
    y = np.arange(-2 * radius, 2 * radius, 0.1)
    
    X, Y = np.meshgrid(x, y)
    
    fxy = X ** 2 + Y ** 2 - radius ** 2
    
    plt.contour(X, Y, fxy, levels=np.linspace(0, 1000, 1000))  
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Circle')
    plt.legend()
    plt.axis('equal')
    plt.savefig('fig_4.png')
    
if __name__ == '__main__':
    circle()