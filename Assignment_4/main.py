from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt
import os
import sys
from PythonRobotics.PathPlanning.ProbabilisticRoadMap import probabilistic_road_map

# field_size = 250

# obstacle_field, coverage = create_obstacle_field(
#     environment = np.zeros((field_size, field_size)), 
#     goal_coverage = 0.1, 
#     obstacle_square_unit= 5)

# os.chdir(r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_4")
# np.save("10_coverage3.npy", obstacle_field)


# plt.figure("Assignment 4 (RBE 550): Firetruck vs. Wumpus")
# plt.subplot(2, 3, (1,4)), 
# plt.imshow(obstacle_field, cmap = "binary"), plt.title(f"{round(coverage * 100)} % Coverage")

# plt.show()


path = r"C:\Users\layhu\OneDrive\Desktop\RBE 550 (Motion Planning)\Assignment_4"

if os.getcwd() is not path: 
    os.chdir(path)
    start_env = np.load(path + r"\10_coverage.npy")


np.set_printoptions(threshold=sys.maxsize)
# print(start_env)

# plt.imshow(start_env, cmap = "binary"), plt.title(f"{10} % Coverage")
plt.show()

iterations = np.nditer(start_env, flags=["multi_index"])


obstacle_x = []
obstacle_y = []
open_x = []
open_y = []

for i in iterations:
    if i == 1: 
        obstacle_x.append(iterations.multi_index[0])
        obstacle_y.append(iterations.multi_index[1])
        # obstacle_x.append()
        # print("%d <%s>" % (i, iterations.multi_index), end=' ')
    else:
        open_x.append(iterations.multi_index[0])
        open_y.append(iterations.multi_index[1])


probabilistic_road_map.prm_planning()
# print(f"x locations: {obstacle_x}, y locations: {obstacle_y}")




# plt.show()