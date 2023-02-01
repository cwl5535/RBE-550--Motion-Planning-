from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt


environment = np.array(
                [[np.ones((1,128))],
                [np.ones((126,1)), np.zeros((126,126)), np.ones((126,1))],
                [np.ones((1,128))]
                ])

print(environment.size, environment.shape)

# obstacle_field, coverage = create_obstacle_field(environment, 0.7)

# plt.imshow(obstacle_field, cmap= "binary")

# plt.show()