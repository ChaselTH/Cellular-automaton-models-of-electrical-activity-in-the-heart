import numpy as np
import matplotlib.pyplot as plt
import math
from cell import Cell

plt.switch_backend('TKAgg')


class Grid:

    def __init__(self, size):
        self.cell_array = []
        plt.ion()
        self.grid = np.zeros((size, size))
        self.raw, self.col = np.shape(self.grid)
        # self.grid = np.array([[1,0,0],[0,0,1],[0,0,1]])
        self.generate_cells()
        self.fig, self.ax = plt.subplots()
        self.draw(self.grid, 0)

    def draw(self, sate_set, t):
        self.ax.pcolor(sate_set, edgecolors='k', linewidth=0.5)
        self.ax.set_aspect('equal')
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.pause(t)

    def onclick(self, event):
        _gx = int(math.floor(event.xdata))
        _gy = int(math.floor(event.ydata))
        current_state = self.grid[_gy, _gx]
        self.grid[_gy, _gx] = self.next_state(current_state)
        # if current_state == 0:
        #     self.grid[_gy, _gx] = 2
        # elif current_state == 1:
        #     self.grid[_gy, _gx] = 0
        # elif current_state == 2:
        #     self.grid[_gy, _gx] = 1
        self.generate_cells()
        while(not self.is_dead()):
            self.update()
        # print(self.get_cell(10, 5).state)
        self.draw(self.grid, 0)

    def generate_cells(self):
        self.cell_array = []
        for x in range(self.col):
            for y in range(self.raw):
                self.cell_array.append(Cell(x, y, self.grid[x, y]))

    def generate_grid(self):
        for cell in self.cell_array:
            self.grid[cell.x, cell.y] = cell.state

    def get_cell(self, x, y):
        return self.cell_array[self.col*y+x]

    def is_in_grid(self, x, y):
        if 0 <= x < self.col and 0 <= y < self.raw:
            return True
        else:
            return False

    def get_up_cell(self, cell):
        if self.is_in_grid(cell.x, cell.y + 1):
            return self.get_cell(cell.x, cell.y + 1)

    def get_down_cell(self, cell):
        if self.is_in_grid(cell.x, cell.y - 1):
            return self.get_cell(cell.x, cell.y - 1)

    def get_left_cell(self, cell):
        if self.is_in_grid(cell.x - 1, cell.y):
            return self.get_cell(cell.x - 1, cell.y)

    def get_right_cell(self, cell):
        if self.is_in_grid(cell.x + 1, cell.y):
            return self.get_cell(cell.x + 1, cell.y)

    def get_around_sell(self, cell):
        cell_list = [self.get_left_cell(cell),
                     self.get_right_cell(cell),
                     self.get_up_cell(cell),
                     self.get_down_cell(cell)]
        return cell_list

    def next_state(self, state):
        if state == 0:
            return 2
        elif state == 2:
            return 1
        elif state == 1:
            return 0

    def is_dead(self):
        for cell in self.cell_array:
            if cell.state != 0:
                return False
        return True

    def update(self):
        for cell in self.cell_array:
            if cell.state != 0:
                cell.state = self.next_state(cell.state)
                for around_cell in self.get_around_sell(cell):
                    if around_cell is not None:
                        self.cell_array[self.col*around_cell.y+around_cell.x].state = self.next_state(around_cell.state)
        self.generate_grid()
        self.draw(self.grid, 0.1)



