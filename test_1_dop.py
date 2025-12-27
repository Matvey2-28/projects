import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def cicloid():

    def cicloid_move(R=3, vx0=0.01, time=10):
        
        x0 = vx0 * time
        t = np.arange(-2 * R, 2 * R, 0.1)
        x = x0 + R * (t - np.sin(t))
        y = R * (1 - np.cos(t))
        return x, y
    
    fig, ax = plt.subplots()
    cicloid, = plt.plot([], [], 'o', color='r', label='Ball')
    cicloid_line, = plt.plot([], [], '-', color='r', label='Trajectory')
        
    frames = 360
    
    
    def animate(i):
        
        cicloid.set_data(cicloid_move(time=i))
        
        return cicloid
    
    
    ax.set_xlim(-2 * np.pi * 3, 2 * np.pi * 3)
    ax.set_ylim(-2 * 3, 2 * 3)
    
    ani = FuncAnimation(fig,
                        animate,
                        frames = frames,
                        interval = 30)
    ani.save('animation_cicloid.gif', writer='pillow')
    
# def astroid():
    
#     def astroid_move(R=5, vx0=0.01, vy0=0.01, time=10):
#         x0 = vx0 * time
#         y0 = vy0 * time
#         t = np.arange(-2 * (R / 4), 2 * R, 0.1)
#         x = x0 + R * np.cos(t) ** 3
#         y = y0 + R * np.sin(t) ** 3
#         return x, y
    
#     fig, ax = plt.subplots()
#     astroid, = plt.plot([], [], 'o', color='r', label='Ball')
#     astroid_line, = plt.plot([], [], '-', color='r', label='Trajectory')
        
#     frames = 360
    
    
#     def animate(i):
        
#         astroid.set_data(cicloid_move(time=i))
        
#         return astroid
    
#     edge = 3
#     ax.axis('equal')
#     ax.set_xlim(-edge, edge)
#     ax.set_ylim(-edge, edge)
    
#     ani = FuncAnimation(fig,
#                         animate,
#                         frames = frames,
#                         interval = 30)
#     ani.save('animation_astroid.gif', writer='pillow')
    
    
if __name__ == '__main__':
    cicloid()
    # astroid()
    
    