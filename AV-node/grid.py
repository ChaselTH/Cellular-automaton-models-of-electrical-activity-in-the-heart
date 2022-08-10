import numpy as np
import matplotlib.pyplot as plt

from cell import Cell


class Grid:

    def __init__(self):
        self.cell_box = []
        self.coordinate_box = []

        self.size = 100

        # build the structure of the AV node
        self.fig = np.zeros((100, 100))

        for y in range(47, 53):
            for x in range(15, 20):
                self.coordinate_box.append((x, y))
            for x in range(80, 85):
                self.coordinate_box.append((x, y))

        for y in range(25, 75):
            for x in range(20, 30):
                self.coordinate_box.append((x, y))
            for x in range(70, 80):
                self.coordinate_box.append((x, y))

        for x in range(25, 75):
            for y in range(25, 35):
                self.coordinate_box.append((x, y))
            for y in range(65, 75):
                self.coordinate_box.append((x, y))

        for coordinate in self.coordinate_box:
            self.fig[coordinate[0], coordinate[1]] = 1

        self.fig[15, 50] = 5
        self.fig[15, 49] = 5
        self.fig[15, 48] = 5
        self.fig[15, 51] = 5

        self.update_cell()

        plt.matshow(self.fig, fignum=0)
        # plt.show()
        self.update()

    def change_cell(self, x, y, want_state, change_state):
        if self.fig[x, y] == want_state:
            self.fig[x, y] = change_state

    def update(self):
        for t in range(10000):
            self.spread(12)
            plt.clf()
            plt.matshow(self.fig, fignum=0)
            plt.pause(0.001)

    def update_cell(self):
        self.cell_box.clear()
        for c in self.coordinate_box:
            self.cell_box.append(Cell(c[0], c[1], self.fig[c[0], c[1]]))

    def update_fig(self):
        for cell in self.cell_box:
            self.fig[cell.x, cell.y] = cell.state

    def calculate_state(self, x, y):
        return self.fig[x+1, y]\
                + self.fig[x, y+1]\
                + self.fig[x-1, y]\
                + self.fig[x, y-1]\
                + self.fig[x+1, y+1]\
                + self.fig[x+1, y-1]\
                + self.fig[x-1, y+1]\
                + self.fig[x-1, y-1]

    def spread(self, threshold):
        for cell in self.cell_box:
            if cell.state == 1:
                state = self.calculate_state(cell.x, cell.y)
                print(state)
                if state > threshold:
                    cell.state = 5
            else:
                cell.next_state()
        self.update_fig()
        self.update_cell()


