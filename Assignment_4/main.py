from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt

field_size = 250

obstacle_field, coverage = create_obstacle_field(
    environment = np.zeros((field_size, field_size)), 
    goal_coverage = 0.1, 
    obstacle_square_unit= 5)

plt.figure("Assignment 4 (RBE 550): Firetruck vs. Wumpus")
# plt.subplot(2, 3, (1,4)), 
plt.imshow(obstacle_field, cmap = "binary"), plt.title(f"{round(coverage * 100)} % Coverage")
plt.show()