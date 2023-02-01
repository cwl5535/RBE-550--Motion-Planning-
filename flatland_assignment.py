from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt


obstacle_field, coverage = create_obstacle_field(np.zeros((128,128)), 0.7)

plt.imshow(obstacle_field)

plt.show()