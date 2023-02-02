from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt
import sys

np.set_printoptions(threshold=sys.maxsize)


# Initial Environment with Closed Border
grid_size = 128
init_env = np.zeros((grid_size, grid_size))

# Adding the borders
init_env[0, 0:grid_size], init_env[1:grid_size-1, 0], init_env[1:(grid_size-1), (grid_size-1)], init_env[(grid_size-1), 0:grid_size] = 1,1,1,1

# Generating the obstacles within the area NOT including the border
obstacle_field, coverage = create_obstacle_field(np.zeros(((grid_size-2),(grid_size-2))), 0.5)  # NOTE that size of environment given to create_obstacle_field is only the area that doesn't include the border from the init_env

# Adding the obstacles to the initial environment
init_env[1:(grid_size-1), 1:(grid_size-1)] = obstacle_field

# Displaying the environment
plt.figure("Assignment 2: Flatland Assignment")
plt.imshow(init_env, cmap= "binary")


plt.show()