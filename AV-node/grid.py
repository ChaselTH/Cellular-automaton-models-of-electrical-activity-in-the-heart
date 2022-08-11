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
            self.fig[coordinate[0], coordinate[1]] = 20

        for y in range(47, 53):
            self.fig[15, y] = 15

        self.update_cell()

        plt.matshow(self.fig, fignum=0)
        # plt.show()
        self.update()

    def update(self):
        for t in range(10000):
            self.spread(3, 0)
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
        state_area = self.fig[x - 2: x + 3, y - 2: y + 3] % 2
        state = state_area.sum()

        return state

    def spread(self, slow, fast):
        for cell in self.cell_box:
            if cell.state == 20:
                state = self.calculate_state(cell.x, cell.y)
                if cell.y < 50 and state > slow:
                    cell.state = 15
                elif cell.y >= 50 and state > fast:
                    cell.state = 15
            else:
                cell.next_state()
        self.update_fig()
        self.update_cell()
