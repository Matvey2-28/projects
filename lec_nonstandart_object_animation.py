import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def circle_move(R, vx0, vy0, time):
    x0 = vx0 * time
    y0 = vy0 * time
    alpha = np.arange(0, 2*np.pi, 0.001)
    x = x0 + R * np.cos(alpha)
    y = y0 + R * np.sin(alpha)
    return x, y

fig, ax = plt.subplots()
ball, = plt.plot([], [], 'o', color='r', label='Ball')
ball_line, = plt.plot([], [], '-', color='r', label='Trajectory')
    
frames = 360
coords = np.zeros((frames, 2))

def animate(i):
    
    ball.set_data(circle_move(R=0.5, vx0=0.01, vy0=0.01, time=i))
    
    return ball

edge = 3
ax.axis('equal')
ax.set_xlim(-edge, edge)
ax.set_ylim(-edge, edge)

ani = FuncAnimation(fig,
                    animate,
                    frames = frames,
                    interval = 30)
ani.save('animation_3.gif', writer='pillow')