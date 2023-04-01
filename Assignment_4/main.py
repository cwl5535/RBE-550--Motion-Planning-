from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt
import os
import sys
from PythonRobotics.PathPlanning.ProbabilisticRoadMap import probabilistic_road_map as prm
from wumpus import Wumpus
from firetruck import Firetruck
from random import randint
import itertools

# Creating an Obstacle Field 
#############################################

# field_size = 250

# obstacle_field, coverage = create_obstacle_field(
#     environment = np.zeros((field_size, field_size)), 
#     goal_coverage = 0.1, 
#     obstacle_square_unit= 5)

# os.chdir(r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_4")
# np.save("10_coverage3.npy", obstacle_field)

################################################################


# plt.figure("Assignment 4 (RBE 550): Firetruck vs. Wumpus")
# plt.subplot(2, 3, (1,4)), 
# plt.imshow(obstacle_field, cmap = "binary"), plt.title(f"{round(coverage * 100)} % Coverage")

# plt.show()

class Obstacle():
    def __init__(self, x, y):
        self.burning = False
        self.burned = False
        self.extinguished = False
        self.intact = True
        self.x = x
        self.y = y

def loadObstacles(desktop: bool, filename: str):
    if desktop: 
        path = r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_4"
    else:
        path = r"C:\Users\layhu\OneDrive\Desktop\RBE 550 (Motion Planning)\Assignment_4"

    if os.getcwd() is not path: 
        os.chdir(path)
        # start_env = np.load(path + r"\10_coverage.npy")
        start_env = np.load(path + filename)


    np.set_printoptions(threshold=sys.maxsize)

    iterations = np.nditer(start_env, flags=["multi_index"])

    obstacle_x = []
    obstacle_y = []
    open_x = []
    open_y = []
    obstacles = []

    for i in iterations:
        if i == 1: 
            x = iterations.multi_index[0]
            y = iterations.multi_index[1]
            obstacle_x.append(x)
            obstacle_y.append(y)

            obstacles.append(Obstacle(x, y))
            
            # obstacle_x.append()
            # print("%d <%s>" % (i, iterations.multi_index), end=' ')
        else:
            open_x.append(iterations.multi_index[0])
            open_y.append(iterations.multi_index[1])


    return obstacle_x, obstacle_y, open_x, open_y, obstacles

# def prm(rng=None):

#     print(__file__ + " start!!")
#     show_animation = True
#     # start and goal position
#     sx = 10.0  # [m]
#     sy = 10.0  # [m]
#     gx = 50.0  # [m]
#     gy = 50.0  # [m]
#     robot_size = 1.0  # [m]

#     ox = obstacle_x
#     oy = obstacle_y

#     if show_animation:
#         plt.plot(ox, oy, ".k")
#         plt.plot(sx, sy, "^r")
#         plt.plot(gx, gy, "^c")
#         plt.grid(True)
#         plt.axis("equal")

#     rx, ry = prm.prm_planning(sx, sy, gx, gy, ox, oy, robot_size)

#     assert rx, 'Cannot find path'

#     if True:
#         plt.plot(rx, ry, "-r")
#         plt.pause(0.001)
#         plt.show()



def main(): 
    obstacle_x, obstacle_y, open_x, open_y, obstacles = loadObstacles(desktop = False, filename = r"\10_coverage.npy")
    t = 0
    burning = []  # obstacle to be extinguished, goal points for the fire truck
    burnable = [] #obstacles that aren't burning or can be relit, goal points for the wumpus -- 
    extinguished = []
    intact = [] 

    for x,y in zip(obstacle_x, obstacle_y):
        intact.append((x,y))
        burnable.append((x,y))
    


    wumpus = Wumpus()
    firetruck = Firetruck()

    wumpusPlanning = True
    firetruckPlanning = True
    wumpusMoving = False
    firetruckMoving = False
    # fire truck does prm initial planning
    
    random_number = randint(0, len(obstacle_x))

    while t < 3600: 
        t += 1


# Wumpus 
        if wumpusPlanning: 
            print("Wumpus is planning...")
            wumpusPlanning = True
            wumpus.path_x, wumpus.path_y = wumpus.plan(obstacle_x, obstacle_y, 10, 10, obstacle_x[random_number], obstacle_y[random_number])
            if wumpus.path_x:
                wumpusPlanning = False
        else:
            wumpus.move(wumpus.path_x, wumpus.path_y)
            wumpusPlanning = True

# Firetruck
        if firetruckPlanning:
            print("Firetruck is planning...")
            firetruckPlanning = True
            firetruck.path_x, firetruck.path_y = firetruck.plan(obstacle_x, obstacle_y, 225, 225, burning[0][0], burning[0][1])

            if firetruck.path_x: 
                firetruckPlanning = False
            else: 
                print("Path not found")
            # fire truck is moving
        else:
            firetruck.move(firetruck.path_x, firetruck.path_y)           
            # stops for 5 seconds
            # any states within 10m are extinguished
            firetruckPlanning = True
            wumpus.plan()



        plt.plot(list(zip(*intact))[0], list(zip(*intact))[1], ".k")
        plt.plot(list(zip(*burning))[0], list(zip(*burning))[1], ".r")
        plt.plot(list(zip(*extinguished))[0], list(zip(*extinguished))[1], ".b")  

        # plt.plot(sx, sy, "^r")
        # plt.plot(gx, gy, "^c")
        plt.grid(True)




















        plt.axis("equal")




if __name__ == '__main__':
    main()


