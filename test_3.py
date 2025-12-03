import matplotlib.pyplot as plt
import numpy as np

def ellipse(x_limits0, x_limits1, y_limits0, y_limits1, N, a = 0.7, b = 0.4):
    
    x = np.arange(x_limits0, x_limits1, N)
    y = np.arange(y_limits0, y_limits1, N)
    X, Y = np.meshgrid(x, y)
    fxy = X**2 / a**2 + Y**2 / b**2 - 1
    
    plt.contour(X, Y, fxy, levels=[0])
    plt.savefig('ellipse.png')
    
if __name__ == '__main__':
    ellipse(-2, 2, -2, 2, 0.01)
    