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

def main(): 
    obstacle_x, obstacle_y, open_x, open_y, obstacles = loadObstacles(desktop = False, filename = r"\10_coverage.npy")
    t = 0
    burning = []  # obstacle to be extinguished, goal points for the fire truck
    burnable = [] #obstacles that aren't burning or can be relit, goal points for the wumpus -- 
    extinguished = []
    intact = [] 
    # obstacle_xys = []

    for x,y in zip(obstacle_x, obstacle_y):
        intact.append((x,y))
        burnable.append((x,y))
        # obstacle_xys.append((x,y))
    
    def burning(x,y):
        burning.append((x,y))
        intact.remove((x,y))
        burnable.remove((x,y))
    
    def extinguished(x,y):
        extinguished.append((x,y))
        burning.remove((x,y))
        burnable.append((x,y))



    wumpus = Wumpus()
    firetruck = Firetruck()
    final_wumpus_path_x = []
    final_wumpus_path_y = []
    final_firetruck_path_x = []
    final_firetruck_path_y = []

    wumpusStart = (10,10)
    firetruckStart = (225,225)

    wumpusPlanning = True
    firetruckPlanning = True
    
    # fire truck does prm initial planning
    


    while t < 3600: 
        random_number = randint(0, len(obstacle_x))
        t += 1

# TODO need to figure out how to implement state transitions from burning to extinguished and etc. 
# Wumpus 
        if wumpusPlanning: 
            print("Wumpus is planning...")
            wumpusPlanning = True
            # wumpus picks a goal based on what is in the burnable list
            wumpus.path_x, wumpus.path_y = wumpus.plan(obstacle_x, obstacle_y, wumpusStart[0], wumpusStart[1], burnable[random_number][0], burnable[random_number][1])
            if wumpus.path_x:
                # if a path has been found, we're going to add the path to the final path, add the obstacle to the `burning` list and remove from the obstacle_xys list
                final_wumpus_path_x.append(wumpus.path_x)
                final_wumpus_path_y.append(wumpus.path_y)
                burning(burnable[random_number][0], burnable[random_number][1])

# Firetruck
        if firetruckPlanning:
            print("Firetruck is planning...")
            firetruckPlanning = True
            firetruck.path_x, firetruck.path_y = firetruck.plan(obstacle_x, obstacle_y, firetruckStart[0], firetruckStart[1], burning[0][0], burning[0][1])

            if firetruck.path_x: 
                final_firetruck_path_x.append(firetruck.path_x)
                final_firetruck_path_y.append(firetruck.path_y)
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







def add_to_burning():
    burning.append((x,y))
















if __name__ == '__main__':
    main()


