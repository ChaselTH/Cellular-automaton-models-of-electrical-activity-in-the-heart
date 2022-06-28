import numpy as np
import matplotlib.pyplot as plt
import time

plt.ion()
for i in range(100):
    plt.clf()
    plt.plot(range(i))
    plt.pause(0.1)

