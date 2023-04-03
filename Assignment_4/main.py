from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt
import os
import sys
from PythonRobotics.PathPlanning.ProbabilisticRoadMap import probabilistic_road_map as prm
from wumpus import Wumpus
from firetruck import Firetruck
from random import randint
from math import hypot
import pickle
import time

# Creating an Obstacle Field 
############################################

# field_size = 250

# obstacle_field, coverage = create_obstacle_field(
#     environment = np.zeros((field_size, field_size)), 
#     goal_coverage = 0.1, 
#     obstacle_square_unit= 5)

# os.chdir(r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_4\Run_5")
# np.save("10_coverage5.npy", obstacle_field)

# ###############################################################


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
    obstacle_x, obstacle_y, open_x, open_y, obstacles = loadObstacles(desktop = True, filename = r"\Run_3\10_coverage3.npy")
    t = 0
    burning = []  # obstacle to be extinguished, goal points for the fire truck
    burnable = [] #obstacles that aren't burning or can be relit, goal points for the wumpus -- 
    extinguished = []
    burned = []
    intact = [] 
    open_goals = []

    intact_sim = []
    burning_sim = []
    extinguished_sim = []
    burned_sim = []


    for x,y in zip(obstacle_x, obstacle_y):
        intact.append((x,y))
        burnable.append((x,y))

    for op_x, op_y in zip(open_x, open_y):
        open_goals.append((op_x, op_y))

    def within_radius(radius, current_position, other_node):
        if hypot((other_node[0] - current_position[0]), (other_node[1] - current_position[1])) <= radius: 
            return True
        return False

    def add_to_burning(x,y,t):
        burning.append((x,y,t))
        intact.remove((x,y))
        burnable.remove((x,y))

    def add_to_burned(x,y,t):
        burned.append((x,y))
        burning.remove((x,y,t))
    
    def add_to_extinguished(x,y,t):
        extinguished.append((x,y))
        burning.remove((x,y,t))
        burnable.append((x,y))



    wumpus = Wumpus()
    firetruck = Firetruck()
    wumpus.finalpath_x = []
    wumpus.finalpath_y = []
    firetruck.finalpath_x = []
    firetruck.finalpath_y = []

    wumpus.start = (10,10)
    firetruck.start = (225,10)

    total_wumpus_CPU_time = 0
    total_firetruck_CPU_time = 0

    wumpus.planning = True
    firetruck.planning = True
    wumpus.waitingToPlan = False
    firetruck.waitingToPlan = False
    firetruck.extinguishing = False
    # fire truck does prm initial planning
    


    while t < 360: 
        random_number = randint(0, len(obstacle_x))
        print(f"t = {t}")
        


 
# Wumpus 
        if wumpus.planning: 
            print("Wumpus is planning...")
            try:
                wumpus.goal_obstacle = burnable[random_number]
            except IndexError:
                wumpus.planning = False
                wumpus.waitingToPlan = False
                print("Wumpus: I have burned everything!!!!!")
            # wumpus picks a goal based on what is in the burnable list
            wump_start_time = time.time_ns()
            wumpus.path_x, wumpus.path_y = wumpus.plan(obstacle_x, obstacle_y, wumpus.start[0], wumpus.start[1],wumpus.goal_obstacle[0],wumpus.goal_obstacle[1])
            wump_end_time = time.time_ns()
            dt_wumpus = wump_end_time - wump_start_time

            if wumpus.path_x:
                print("Wumpus path found!")
                # if a path has been found, we're going to add the path to the final path, add the obstacle to the `burning` list and remove from the obstacle_xys list
                wumpus.finalpath_x.append(wumpus.path_x)
                wumpus.finalpath_y.append(wumpus.path_y)
                add_to_burning(wumpus.goal_obstacle[0], wumpus.goal_obstacle[1], t)  # set obstacle to burning
                wumpus.planning = False
                wumpus.waitingToPlan = True
                wumpus.waitCounter = 0
                wumpus.start = wumpus.goal_obstacle
            else: 
                print("Path not found for wumpus")

        elif wumpus.waitingToPlan:
            print("Wumpus is waiting...")
            wumpus.waitCounter += 1
            
            if wumpus.waitCounter == 10:
                for obstacle in burnable:
                    if within_radius(30, (wumpus.goal_obstacle[0],wumpus.goal_obstacle[1]), obstacle):
                        add_to_burning(obstacle[0], obstacle[1], t)
            elif wumpus.waitCounter == len(wumpus.path_x):   # wumpus will wait to begin another plan for as long as it would take it to move, assuming each timestep to move, t, is one iteration
                wumpus.waitingToPlan = False
                wumpus.planning = True

# time check to see if burning obstacles have completely burned
        for b in burning: 
            if abs(t - b[2]) >= 25: 
                add_to_burned(b[0], b[1], b[2])


# Firetruck
        # burning = [(x,y) for x,y in zip(range(50), range(50))]


        if firetruck.planning:
            if len(burning) > 1:
                random_burning_number = randint(0, len(burning))
                firetruck.goal_obstacle = firetruck.search_for_nearby_open(burning[random_burning_number], open_goals)
            else: # no items are burning
                random_burning_number = 0
                firetruck.goal_obstacle = (wumpus.x, wumpus.y) # hunt for the wumpus

            print(f"random burning number = {random_burning_number}")
            print(f"burning is {len(burning)} elements long")
            print(f"burned is {len(burned)} elements long") 
              

            # firetruck.goal_obstacle = firetruck.search_for_nearby_open(burning[0], open_goals)
            assert firetruck.goal_obstacle is not None
            print("Firetruck is planning...")

            firetruck_start_time = time.time_ns()
            firetruck.path_x, firetruck.path_y = firetruck.plan(obstacle_x, obstacle_y, firetruck.start[0], firetruck.start[1], firetruck.goal_obstacle[0], firetruck.goal_obstacle[1])
            
            firetruck_end_time = time.time_ns()
            dt_firetruck = firetruck_end_time - firetruck_start_time
            
            
            if firetruck.path_x: 
                print("Firetruck path found!")
                firetruck.finalpath_x.append(firetruck.path_x)
                firetruck.finalpath_y.append(firetruck.path_y)
                firetruck.planning = False
                firetruck.waitingToPlan = True
                firetruck.waitCounter = 0
                firetruck.start = firetruck.goal_obstacle
            else: 
                print("Path not found for firetruck")

        elif firetruck.waitingToPlan:            # fire truck is moving
            print("Firetruck is waiting...")
            firetruck.waitCounter += 1
            if firetruck.waitCounter == len(firetruck.path_x):  # firetruck will wait for as long as the amount of points exist for it to move
                firetruck.waitingToPlan = False
                firetruck.extinguishing = True
                firetruck.extCounter = 0

        elif firetruck.extinguishing: 
            print("Firetruck is extinguishing fires!")
            firetruck.extCounter += 1
            if firetruck.extCounter == 5:  # if the firetruck waits for 5 seconds, obstacles within 10 m will be extinguished
                for burning_obstacle in burning:
                    if within_radius(10, firetruck.goal_obstacle, burning_obstacle):
                        add_to_extinguished(burning_obstacle[0], burning_obstacle[1], burning_obstacle[2])
                
                firetruck.extinguishing = False
                firetruck.planning = True

        
        intact_sim.append(intact)
        burning_sim.append(burning)
        extinguished_sim.append(extinguished)
        burned_sim.append(burned)

        total_wumpus_CPU_time += dt_wumpus
        total_firetruck_CPU_time += dt_firetruck

        # if intact: 
        #     plt.plot(list(zip(*intact))[0], list(zip(*intact))[0], ".g")
        # if burning:
        #     plt.plot(list(zip(*burning))[0], list(zip(*burning))[0], ".r")
        # if extinguished: 
        #     plt.plot(list(zip(*extinguished))[0], list(zip(*extinguished))[0], ".b")  
        # if burned:
        #     plt.plot(list(zip(*burned))[0], list(zip(*burned))[0], ".k")

        # plt.pause(0.001)
        # plt.show()
        # plt.pause(0.001)
        
        t += 1

        # plt.plot(sx, sy, "^r")
        # plt.plot(gx, gy, "^c")
        # plt.grid(True)
        # plt.axis("equal")
        # plt.show()
    
    # each sim list is a list of lists of tuples 

    # if intact_sim: 
    #     plt.plot(list(zip(*intact_sim))[0], list(zip(*intact_sim))[1], ".k")
    # if burning_sim:
    #     plt.plot(list(zip(*burning_sim))[0], list(zip(*burning_sim))[1], ".r")
    # if extinguished_sim: 
    #     plt.plot(list(zip(*extinguished_sim))[0], list(zip(*extinguished_sim))[1], ".b") 


    # Saving Variables
    """
    wumpus.finalpath_x
    wumpus.finalpath_y
    firetruck.finalpath_x
    firetruck.finalpath_y
    intact_sim
    burning_sim
    burned_sim
    extinguished_sim
    t
    
    """
    os.chdir(r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_4\Run_3")
    with open("CPU_times_run3.txt", "wb") as c:
        pickle.dump([total_wumpus_CPU_time, total_firetruck_CPU_time, np.arange(0, t)], c)
    with open("simulation_variables_run3.txt", "wb") as s: 
        pickle.dump([intact_sim, burning_sim, burned_sim, extinguished_sim, t],s)

    with open("wumpus_path_run3.txt", "wb") as w: 
        pickle.dump([wumpus.finalpath_x, wumpus.finalpath_y], w)

    with open("firetruck_path_run3.txt", "wb") as f: 
        pickle.dump([firetruck.finalpath_x, firetruck.finalpath_y], f)

    # plt.grid(True)
    # plt.axis("equal")
    # plt.pause(0.001)
    # plt.show()



if __name__ == '__main__':
    main()


