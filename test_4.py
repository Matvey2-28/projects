import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


fig, ax = plt.subplots()
anim_object, = plt.plot([], [])

x, y = [], []

t = 500
C = 0.3
D = 0.33
x0 = 0.1
y0 = 0.1
x.append(x0)
y.append(y0)

plt.xlim(-8, 8)
plt.ylim(-8, 8)


def update(t):
    
    x0 = x[t]
    y0 = y[t]
    x1 = x ** 2 - y ** 2 + C
    y1 = 2 * x * y + D
    x.append(x1)
    y.append(y1)
    
    anim_object.set_data(x, y)
    return anim_object,

ani = FuncAnimation(fig,
                    update,
                    frames = t,
                    interval = 60)
ani.save('fraktal.gif', writer='pillow')   
    
    