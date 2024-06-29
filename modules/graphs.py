import matplotlib.pyplot as plt
import numpy as np

def graph(x, y, title, x_axis_label, y_axis_label):
    x = np.array(x)
    y = np.array(y)
    plt.title(title)
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.xticks(rotation=45)
    plt.plot(x, y)
    plt.show()