import numpy as np
import matplotlib.pyplot as plt
import math

plt.switch_backend('TKAgg')


class Grid:

    def __init__(self, size):
        plt.ion()
        self.grid = np.zeros((size, size))
        self.fig, self.ax = plt.subplots()
        self.draw()

    def draw(self):
        self.ax.pcolor(self.grid, edgecolors='k', linewidth=0.5)
        self.ax.set_aspect('equal')
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.pause(0)

    def onclick(self, event):
        _gx = int(math.floor(event.xdata))
        _gy = int(math.floor(event.ydata))
        current_state = self.grid[_gy, _gx]
        print(current_state)
        if current_state == 0:
            self.grid[_gy, _gx] = 1
        else:
            self.grid[_gy, _gx] = 0
        self.draw()
        plt.clf()
