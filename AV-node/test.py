import numpy as np
import matplotlib.pyplot as plt
import time

plt.ion()
for i in range(200):

    plt.plot(range(i))
    plt.draw()
    time.sleep(0.5)
    plt.ioff()
    plt.show()


