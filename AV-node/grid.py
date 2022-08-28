import random
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as ma
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
        self.resize(1200, 800)

        self.x_record = []
        self.y_record = []
        self.y_converse = []
        self.x_record.append(0)
        self.y_record.append(0)
        self.y_converse.append(0)

        self.check_point = 0

        self.cell_box = []
        self.coordinate_box = []
        self.size = 100
        self.grid = np.zeros((100, 100))
        self.activate = 33

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)

        self.s_f_avnrt = QtWidgets.QPushButton("slow-fast AVNRT")
        self.f_s_avnrt = QtWidgets.QPushButton("fast-slow AVNRT")
        self.start = QtWidgets.QPushButton("Start")
        self.pace_btn = QtWidgets.QPushButton("Send Impulse")
        self.counter_pace_btn = QtWidgets.QPushButton("Counter Impulse")

        self.set_freq = QSlider()
        # self.set_freq.setSingleStep(2)
        self.set_freq.setRange(1, 100)
        self.set_freq.setValue(50)
        self.set_freq.valueChanged.connect(self.freq_change)
        self.beat_frq = QLabel("Frequency Lv: " + str(self.set_freq.value()))

        self.stop_btn = QtWidgets.QPushButton("Stop")

        self.freq = self.set_freq.value() * 10

        wlayout = QHBoxLayout()
        hlayout = QHBoxLayout()
        glayout = QGridLayout()

        hlayout.addWidget(self.canvas)
        glayout.addWidget(self.start, 0, 0)
        glayout.addWidget(self.stop_btn, 0, 1)
        glayout.addWidget(self.beat_frq, 1, 0)
        glayout.addWidget(self.set_freq, 1, 1)
        glayout.addWidget(self.s_f_avnrt, 2, 0)
        glayout.addWidget(self.f_s_avnrt, 2, 1)
        glayout.addWidget(self.pace_btn, 3, 0)
        glayout.addWidget(self.counter_pace_btn, 3, 1)

        self.s_f_avnrt.clicked.connect(self.slow_fast)
        self.f_s_avnrt.clicked.connect(self.fast_slow)
        self.pace_btn.clicked.connect(self.beat)
        self.start.clicked.connect(self.start_beat)
        self.stop_btn.clicked.connect(self.stop)
        self.counter_pace_btn.clicked.connect(self.counter_beat)

        hwg = QWidget()
        vwg = QWidget()

        hwg.setLayout(hlayout)
        vwg.setLayout(glayout)

        wlayout.addWidget(hwg)
        wlayout.addWidget(vwg)

        self.setLayout(wlayout)

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

        grid = plt.GridSpec(6, 4, wspace=0.5, hspace=0.5)

        plt.subplot(grid[0:4, 0:4])
        plt.matshow(self.grid, fignum=0)
        plt.axis("off")

        plt.subplot(grid[4:6, 0:4])
        plt.xlim(0, 100)
        plt.ylim(-200, 3200)
        plt.grid(linestyle=':')

        self.canvas.draw()

    def stop(self):
        self.freq = 100000000

    def freq_change(self, event):
        self.freq = int(self.set_freq.value()/100 * 30 + 20)
        self.beat_frq.setText("Frequency LV: " + str(self.set_freq.value()))

    def start_beat(self, event):
        self.check_point = self.x_record[-1]
        self.freq = int(self.set_freq.value()/100 * 30 + 20)
        self.update(True)

    def slow_fast(self, event):
        self.check_point = self.x_record[-1]
        self.freq = 25
        self.update(False)

    def fast_slow(self, event):
        self.check_point = self.x_record[-1]
        self.freq = 40
        self.update(False, True)

    def update(self, reset, counter=False):
        self.make_pace()

        delay = 0
        for t in range(10000):
            delay += 1
            if delay == self.freq:
                if counter:
                    self.counter_pace()
                else:
                    self.make_pace()
                if reset:
                    delay = 0
            self.spread(7, 3)

            plt.clf()
            grid = plt.GridSpec(6, 4, wspace=0.5, hspace=0.5)
            plt.subplot(grid[0:4, 0:4])
            plt.matshow(self.grid, fignum=0)
            plt.axis("off")

            self.x_record.append(t+self.check_point)
            print(self.x_record[-1])
            self.y_record.append(self.in_impulse_update())
            self.y_converse.append(self.out_impulse_update())

            plt.subplot(grid[4:6, 0:4])
            plt.xlim(0, 100)
            plt.ylim(-200, 3200)
            if self.x_record[-1] > 70:
                plt.xlim(self.x_record[-1] - 70, self.x_record[-1] + 70)
            plt.plot(self.x_record, self.y_record, label='in')
            plt.plot(self.x_record, self.y_converse, label="out")
            plt.grid(linestyle=':')

            self.canvas.draw()
            QApplication.processEvents()
            time.sleep(0.0001)

    def in_impulse_update(self):
        state_area = self.grid[5:10, 45:55]
        return 5000 - state_area.sum()

    def out_impulse_update(self):
        state_area = self.grid[90:95, 45:55]
        return 5000 - state_area.sum()

    def opposite_pace(self, event):
        for y in range(45, 55):
            self.grid[94, y] = self.activate
        self.update_cell()

    def beat(self, event):
        self.make_pace()

    def counter_beat(self, event):
        self.counter_pace()

    def make_pace(self):
        for y in range(45, 55):
            self.grid[5, y] = self.activate
        self.update_cell()

    def counter_pace(self):
        for y in range(45, 55):
            self.grid[94, y] = self.activate
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
        return state_area.sum()

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
