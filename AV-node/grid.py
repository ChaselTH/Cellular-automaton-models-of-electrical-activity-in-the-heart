import random
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import Button
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from cell import Cell

matplotlib.use('Qt5Agg')


class Grid(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        self.cell_box = []
        self.coordinate_box = []
        self.size = 100
        self.grid = np.zeros((100, 100))
        self.activate = 33

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)

        self.s_f_avnrt = QtWidgets.QPushButton("slow-fast AVNRT")
        self.start = QtWidgets.QPushButton("Start")
        self.pace_btn = QtWidgets.QPushButton("Activate")

        self.beat_frq = QLabel("Frequency Lv")
        self.set_freq = QSpinBox()
        self.set_freq.setRange(1, 5)
        self.set_freq.valueChanged.connect(self.freq_change)

        self.freq = self.set_freq.value() * 10

        wlayout = QHBoxLayout()
        hlayout = QHBoxLayout()
        glayout = QGridLayout()

        hlayout.addWidget(self.canvas)
        glayout.addWidget(self.start, 0, 0)
        glayout.addWidget(self.beat_frq, 0, 1)
        glayout.addWidget(self.set_freq, 0, 2)
        glayout.addWidget(self.s_f_avnrt, 1, 0)
        glayout.addWidget(self.pace_btn, 3, 0)

        # layout.addWidget(self.canvas, 0)
        # layout.addWidget(self.s_f_avnrt, 0)
        # layout.addWidget(self.pace_btn, 1)
        # layout.addWidget(self.beat_frq, 2)

        self.s_f_avnrt.clicked.connect(self.slow_fast)
        self.pace_btn.clicked.connect(self.beat)
        self.start.clicked.connect(self.start_beat)

        hwg = QWidget()
        vwg = QWidget()

        hwg.setLayout(hlayout)
        vwg.setLayout(glayout)

        wlayout.addWidget(hwg)
        wlayout.addWidget(vwg)

        self.setLayout(wlayout)

        # self.setLayout(hlayout)
        # self.setLayout(vlayout)
        # wl.addLayout(hlayout)
        # wl.addLayout(vlayout)

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

        plt.axis("off")

        print(222)

        self.canvas.draw()

    def freq_change(self, event):
        self.freq = self.set_freq.value() * 10

    def start_beat(self, event):
        self.update(True)

    def slow_fast(self, event):
        self.freq = 25
        self.update(False)

    def update(self, reset):
        self.make_pace()

        delay = 0
        for t in range(10000):
            delay += 1
            if delay == self.freq:
                self.make_pace()
                if reset:
                    delay = 0
            self.spread(7, 3)
            plt.clf()
            plt.matshow(self.grid, fignum=0)
            plt.axis("off")
            self.canvas.draw()
            QApplication.processEvents()
            time.sleep(0.0001)

    def opposite_pace(self, event):
        for y in range(45, 55):
            self.grid[94, y] = self.activate
        self.update_cell()

    def beat(self, event):
        self.make_pace()

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
