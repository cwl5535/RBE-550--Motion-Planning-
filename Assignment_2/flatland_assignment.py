from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt
import sys

np.set_printoptions(threshold=sys.maxsize)

# Initial Environment with Closed Border
init_env = np.zeros((128,128))

# Adding the borders
init_env[0, 0:128], init_env[1:127, 0], init_env[1:127, 127], init_env[127, 0:128] = 1,1,1,1

# Generating the obstacles
obstacle_field, coverage = create_obstacle_field(np.zeros((126,126)), 0.05)  # NOTE that size of environment given to create_obstacle_field is only the area that doesn't include the border from the init_env
# Adding the obstacles to the initial environment
init_env[1:127, 1:127] = obstacle_field

plt.imshow(init_env, cmap= "binary")

plt.show()