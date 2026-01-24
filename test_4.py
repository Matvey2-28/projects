import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def fractal_move(n):
    n = np.arange(0, 2*np.pi, 0.001)
    C=0.3
    D=0.33
    x0 = 0.1
    y0 = 0.1
    x = (x0 ** 2) * n - (y0 ** 2) * n + C
    y = (2 * x0 * y0) * n + D
    return x, y

fig, ax = plt.subplots()
anim_object, = plt.plot([], [])

x, y = [], []

t = 500
plt.axis('equal')
plt.xlim(-2, 2)
plt.ylim(-2, 2)


def animate(t):
    
    anim_object.set_data(fractal_move(n=t))
    return anim_object,

ani = FuncAnimation(fig,
                    animate,
                    frames = t,
                    interval = 60)
ani.save('fraktal.gif', writer='pillow')   
    
    