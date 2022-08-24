import random
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import Button
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from cell import Cell

matplotlib.use('Qt5Agg')


class Grid(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

        self.cell_box = []
        self.coordinate_box = []
        self.size = 100
        self.grid = np.zeros((100, 100))
        self.activate = 33

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)

        self.button_plot = QtWidgets.QPushButton("123123")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button_plot)

        self.button_plot.clicked.connect(self.update)

        self.setLayout(layout)

        self.reset()

    def reset(self):
        plt.clf()
        self.grid = np.zeros((100, 100))

        for y in range(45, 55):
            for x in range(5, 20):
                self.coordinate_box.append((x, y))
            for x in range(80, 95):
                self.coordinate_box.append((x, y))

        for y in range(0, 100):
            for x in range(0, 100):
                if 20 <= ((x - 49)**2 + (y - 50)**2)**0.5 < 35:
                    self.coordinate_box.append((x, y))

        for coordinate in self.coordinate_box:
            self.grid[coordinate[0], coordinate[1]] = 100

        self.update_cell()

        plt.matshow(self.grid, fignum=0)

        print(222)

        self.canvas.draw()

    def update(self, event):
        self.make_pace()
        delay = 0

        for t in range(10000):
            delay += 1
            if delay == 25:
                self.make_pace()
            self.spread(7, 3)
            plt.clf()
            plt.matshow(self.grid, fignum=0)
            self.canvas.draw()
            plt.pause(0.01)

    def opposite_pace(self, event):
        for y in range(45, 55):
            self.grid[94, y] = self.activate
        self.update_cell()

    def make_pace(self):
        for y in range(45, 55):
            self.grid[5, y] = self.activate
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
            self.cell_box.append(Cell(c[0], c[1], self.grid[c[0], c[1]]))

    def update_grid(self):
        for cell in self.cell_box:
            self.grid[cell.x, cell.y] = cell.state

    def calculate_state(self, x, y):
        state_area = self.grid[x - 4: x + 5, y - 4: y + 5] % 2
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
        self.update_grid()
        # self.update_cell()
