import numpy as np
import matplotlib.pyplot as plt


class Grid:

    def __init__(self, size):
        self.size = size

        self.x_sig = 13
        self.y_sig = 50

        self.sig = []
        self.sig.append([self.x_sig, self.y_sig])

        self.fig = np.zeros((size, size))
        for x in range(10, 16):
            for y in range(47, 53):
                self.fig[x, y] = 1

        for x in range(16, 70):
            for y in range(48, 49):
                self.fig[x, y] = 1
            for y in range(51, 52):
                self.fig[x, y] = 1

        for x in range(69, 70):
            for y in range(30, 48):
                self.fig[x, y] = 1
            for y in range(52, 70):
                self.fig[x, y] = 1

        for x in range(35, 70):
            for y in range(30, 31):
                self.fig[x, y] = 1
            for y in range(69, 70):
                self.fig[x, y] = 1

        self.fig[self.sig[0][0], self.sig[0][1]] = 2
        plt.matshow(self.fig, fignum=0)
        # plt.show()
        self.update()

    def change_cell(self, x, y, want_state, change_state):
        if self.fig[x, y] == want_state:
            self.fig[x, y] = change_state

    def sig_move(self, sig):
        if self.fig[sig[0] - 1, sig[1]] == 1:
            self.fig[sig[0] - 1, sig[1]] = 2
            self.sig.append([sig[0] - 1, sig[1]])

        if self.fig[sig[0], sig[1] - 1] == 1:
            self.fig[sig[0], sig[1] - 1] = 2
            self.sig.append([sig[0], sig[1] - 1])

        if self.fig[sig[0], sig[1] + 1] == 1:
            self.fig[sig[0], sig[1] + 1] = 2
            self.sig.append([sig[0], sig[1] + 1])

        if self.fig[sig[0] + 1, sig[1]] == 1:
            self.fig[sig[0] + 1, sig[1]] = 2
            self.sig.append([sig[0] + 1, sig[1]])

        self.sig.remove(sig)

    def update(self):
        for t in range(10000):
            for sig in self.sig:
                self.sig_move(sig)

            plt.clf()
            plt.matshow(self.fig, fignum=0)
            plt.pause(0.001)
