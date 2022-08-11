import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

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
            for x in range(60, 65):
                self.coordinate_box.append((x, y))

        for y in range(25, 75):
            for x in range(20, 30):
                self.coordinate_box.append((x, y))
            for x in range(50, 60):
                self.coordinate_box.append((x, y))

        for x in range(25, 60):
            for y in range(25, 35):
                self.coordinate_box.append((x, y))
            for y in range(65, 75):
                self.coordinate_box.append((x, y))

        # for x in range(65, 90):
        #     for y in range(45, 48):
        #         self.coordinate_box.append((x, y))
        #     for y in range(52, 55):
        #         self.coordinate_box.append((x, y))

        for coordinate in self.coordinate_box:
            self.fig[coordinate[0], coordinate[1]] = 20

        self.update_cell()

        plt.matshow(self.fig, fignum=0)

        plt.subplots_adjust(bottom=0.2)

        normal_button = plt.axes([0.1, 0.05, 0.1, 0.075])
        normal_button = Button(normal_button, 'normal')
        normal_button.on_clicked(self.update)

        plt.show()


        # self.update()

    def update(self, event):
        break_next = False
        for y in range(47, 53):
            self.fig[15, y] = 15
        self.update_cell()
        for t in range(10000):
            if break_next:
                plt.figure()
                break
            if self.is_cool():
                break_next = True
            self.spread(5, 2)
            plt.clf()
            plt.matshow(self.fig, fignum=0)
            plt.pause(0.001)

    def is_cool(self):
        cool = True
        for cell in self.cell_box:
            if cell.state != 20:
                cool = False
                break
        return cool

    def update_cell(self):
        self.cell_box.clear()
        for c in self.coordinate_box:
            self.cell_box.append(Cell(c[0], c[1], self.fig[c[0], c[1]]))

    def update_fig(self):
        for cell in self.cell_box:
            self.fig[cell.x, cell.y] = cell.state

    def calculate_state(self, x, y):
        state_area = self.fig[x - 3: x + 4, y - 3: y + 4] % 2
        state = state_area.sum()

        return state

    def spread(self, slow, fast):
        for cell in self.cell_box:
            if cell.state == 20:
                state = self.calculate_state(cell.x, cell.y)
                if cell.y < 50 and state >= slow:
                    cell.state = 15
                elif cell.y >= 50 and state >= fast:
                    cell.state = 15
            else:
                cell.next_state()
        self.update_fig()
        self.update_cell()
