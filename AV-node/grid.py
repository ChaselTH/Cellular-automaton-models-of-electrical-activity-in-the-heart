import numpy as np
import matplotlib.pyplot as plt
import math

plt.switch_backend('TKAgg')


class Grid:

    def __init__(self, size):
        plt.ion()
        # self.grid = np.array([[1, 0, 1], [0, 0, 1], [1, 0, 0]])
        self.grid = np.zeros((size, size))
        self.draw(self.grid)
        plt.ioff()
        plt.show()

    def draw(self, state_set):
        plt.ion()
        fig, ax = plt.subplots()
        ax.pcolor(state_set, edgecolors='k', linewidth=0.5)
        ax.set_aspect('equal')
        fig.canvas.mpl_connect('button_press_event', self.onclick)
        fig.canvas.draw()
        fig.canvas.flush_events()

    def onclick(self, event):
        plt.close()
        _gx = int(math.floor(event.xdata))
        _gy = int(math.floor(event.ydata))
        current_state = self.grid[_gy, _gx]
        print(current_state)
        if current_state == 0:
            self.grid[_gy, _gx] = 1
        else:
            self.grid[_gy, _gx] = 0
        self.draw(self.grid)





