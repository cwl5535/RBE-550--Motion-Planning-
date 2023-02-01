from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt
import sys

np.set_printoptions(threshold=sys.maxsize)

# Initial Environment with Closed Border
init_env = np.zeros((128,128))
init_env[0, 0:128], init_env[1:127, 0], init_env[1:127, 127], init_env[127, 0:128] = 1,1,1,1

obstacle_field, coverage = create_obstacle_field(init_env, 0.05)

plt.imshow(obstacle_field, cmap= "binary")

plt.show()