import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation



fig, ax = plt.subplots()
anim_object, = plt.plot([], [])
    
x, y = [], []

t = np.linspace(0, 12 * np.pi, 500)    
    
ax.axis('equal')
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)


def update(t):
    x.append(np.sin(t) * (np.e ** np.cos(t) - 2 * np.cos(4 * t) + np.sin(t / 12) ** 5))
    y.append(np.cos(t) * (np.e ** np.cos(t) - 2 * np.cos(4 * t) + np.sin(t / 12) ** 5))
    
    anim_object.set_data(x, y)
    return anim_object,




ani = FuncAnimation(fig,
                    update,
                    frames = t,
                    interval = 60)
ani.save('animation_butterfly.gif', writer='pillow')