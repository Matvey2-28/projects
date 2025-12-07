import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def circle_move(time):
    alpha = np.arange(0, 2*np.pi, 0.001)
    x = (alpha * time) * np.cos(alpha) * time
    y = (alpha * time) * np.sin(alpha) * time
    return x, y

fig, ax = plt.subplots()

circle_object, = plt.plot([], [], 'o', lw=2)
circle_object_trajectory, = plt.plot([], [], '-')

frames = 360
coords = np.zeros((frames, 2))

def animate(i):
    
    circle_object.set_data(circle_move(time=i))
    
    return circle_object

edge = 3
ax.axis('equal')
ax.set_xlim(-edge, edge)
ax.set_ylim(-edge, edge)

ani = FuncAnimation(fig,
                    animate,
                    frames = frames,
                    interval = 30)
ani.save('animation_circle_radius.gif', writer='pillow')