from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np


def circle_move(R, time):
    x0 = time * 2
    alpha = np.arange(0, 2.5*np.pi, 0.1)
    x = x0 + R * np.cos(alpha)
    y = R * np.sin(alpha)
    return x, y

fig, ax = plt.subplots()
ball, = plt.plot([], [], 'o', color='r', label='Ball')


def animate(i):
    ball.set_data(circle_move(R=i, time=i))
    return ball


edge = 3
plt.axis('equal')
ax.set_xlim(-edge, edge)
ax.set_ylim(-edge, edge)

ani = FuncAnimation(fig, animate, frames=np.arange(0, 3, 0.1), interval=30)
ani.save('circle_zoom_animation.gif', writer="pillow")