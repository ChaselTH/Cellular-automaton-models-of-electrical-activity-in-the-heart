import matplotlib.pyplot as plt
from grid import *
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Grid()
    window.show()
    app.exec()
