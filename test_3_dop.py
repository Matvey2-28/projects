import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def star_move(alpha):
    
    y0 = 1 * alpha
    x0 = 1 * alpha
    R = 5
    x1 = x0
    y1 = -R + y0
    t = np.linspace(0, 4 * np.pi, 100)  
    x = R * np.cos(t) ** 3
    y = R * np.sin(t) ** 3
    
    X = x0 + (x - x1) * np.cos(alpha) - (y - y1) * np.sin(alpha)
    Y = y0 + (y - y1) * np.cos(alpha) + (x - x1) * np.sin(alpha)
    return X, Y


fig, ax = plt.subplots()
star, = plt.plot([], [], color='r', label='Star')
X, Y = [], []    
    
edge = 25

def animate(alpha):
     
    star.set_data(star_move(alpha))
    
    return star

ax.axis('equal')
ax.set_xlim(-edge, edge)
ax.set_ylim(-edge, edge)

ani = FuncAnimation(fig,
                    animate,
                    frames = np.linspace(0, 2 * np.pi, 100),
                    interval = 30)
ani.save('animation_star.gif', writer='pillow')
