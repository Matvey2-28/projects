import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def butterfly_move(t=np.arange(0, 12*np.pi, 0.01)):
    
    x = np.sin(t) * ((np.exp ** np.cos(t)) - 2 * np.cos(4 * t) + np.sin(t / 12) ** 5)
    y = np.cos(t) * ((np.exp ** np.cos(t)) - 2 * np.cos(4 * t) + np.sin(t / 12) ** 5)
    return x, y

fig, ax = plt.subplots()
butterfly, = plt.plot([], [], 'o', color='r', label='Ball')
butterfly_line, = plt.plot([], [], '-', color='r', label='Trajectory')

frames = 360

def animate(i):
    
    butterfly.set_data(butterfly_move(t=i))
    
    return butterfly

ax.axis('equal')
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

ani = FuncAnimation(fig,
                    animate,
                    frames = frames,
                    interval = 60)
ani.save('animation_butterfly.gif', writer='pillow')