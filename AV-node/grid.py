import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from cell import Cell


class Grid:

    def __init__(self):
        self.cell_box = []
        self.coordinate_box = []
        self.size = 100
        self.fig = np.zeros((100, 100))
        self.activate = 33

        self.reset()

    def reset(self):
        plt.clf()
        self.fig = np.zeros((100, 100))

        for y in range(46, 54):
            for x in range(15, 20):
                self.coordinate_box.append((x, y))
            for x in range(80, 85):
                self.coordinate_box.append((x, y))

        for y in range(25, 75):
            for x in range(20, 30):
                self.coordinate_box.append((x, y))
            for x in range(70, 80):
                self.coordinate_box.append((x, y))

        for x in range(30, 70):
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
            self.fig[coordinate[0], coordinate[1]] = 100

        self.update_cell()

        plt.matshow(self.fig, fignum=0)

        plt.subplots_adjust(bottom=0.2)

        normal_button = plt.axes([0.1, 0.05, 0.2, 0.075])
        normal_button = Button(normal_button, 'slow-fast AVNRT')
        normal_button.on_clicked(self.update)

        AVNRT_button = plt.axes([0.5, 0.05, 0.2, 0.075])
        AVNRT_button = Button(AVNRT_button, 'fast-slow AVNRT')
        # AVNRT_button.on_clicked(self.AVNRT_spread)

        print(222)

        plt.show()

        # self.update()

    def update(self, event):
        break_next = False
        self.make_pace()
        delay = 0

        for t in range(10000):
            delay += 1
            if delay == 30:
                self.make_pace()
                delay = 0
            # if break_next:
            #     self.reset()
            #     break
            # if self.is_cool():
            #     break_next = True
            self.spread(7, 1)
            plt.clf()
            plt.matshow(self.fig, fignum=0)
            plt.pause(0.001)

    def make_pace(self):
        for y in range(46, 54):
            self.fig[15, y] = self.activate
        self.update_cell()

    def is_cool(self):
        cool = True
        for cell in self.cell_box:
            if cell.state != 100:
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
        state_area = self.fig[x - 4: x + 5, y - 4: y + 5] % 2
        state = state_area.sum()

        return state

    def spread(self, slow, fast):
        for cell in self.cell_box:
            if cell.state > 76:
                state = self.calculate_state(cell.x, cell.y)
                if cell.y < 50:
                    if state >= slow:
                        cell.state = self.activate
                else:
                    if state >= fast:
                        cell.state = self.activate
            else:
                if cell.y < 50:
                    cell.next_slow()
                else:
                    cell.next_fast()
        self.update_fig()
        # self.update_cell()
