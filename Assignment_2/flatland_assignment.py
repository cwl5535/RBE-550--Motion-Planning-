from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import sys

def place_robot(starting_quadrant, obstacle_field):
    
    obs_field_height = obstacle_field.shape[0]
    obs_field_width = obstacle_field.shape[1]


    # cutting the environment up into 4 quadrants
    if starting_quadrant == "NW":
        environment = obstacle_field[0:((obs_field_height//2)-1), 0:((obs_field_height//2)-1)]
    elif starting_quadrant == "NE":
        environment = obstacle_field[0:((obs_field_height//2)-1), (obs_field_width//2):(obs_field_width)]
    elif starting_quadrant == "SW":
        environment = obstacle_field[(obs_field_width//2):(obs_field_width), 0:((obs_field_height//2)-1)]
    elif starting_quadrant == "SE":
        environment = obstacle_field[(obs_field_width//2):(obs_field_width), (obs_field_width//2):(obs_field_width)]

# iterating through quadrant to find an open spot to land in 
    for row in range(environment.shape[0]):
        for col in range(environment.shape[1]):
            if (environment[row][col] == 0):  # placing robot wherever there is a free space
                break
        else:
            continue   # see https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
        break
    
    obstacle_field[row, col] = np.nan # making the robot a value that isn't 0 or 1 for a different color
    return row, col, obstacle_field


def check_surroundings(environment, current_locations: list) -> list:
    nodes_to_explore = []
    for location in current_locations: 
        row = location[0]
        col = location[1] 

        # surroundings = {(row-1, col-1): environment[row-1, col-1],    (row-1, col): environment[row-1, col],     (row-1, col+1): environment[row-1, col+1],
        #                 (row,   col-1): environment[row,   col-1],                                               (row,   col+1): environment[row,   col+1], 
        #                 (row+1, col-1): environment[row+1, col-1],    (row+1, col): environment[row+1, col],     (row+1, col+1): environment[row+1, col+1] }
        
        surroundings = {                                          (row-1, col): environment[row-1, col],
                        (row,   col-1): environment[row,   col-1],                                               (row,   col+1): environment[row,   col+1], 
                                                                  (row+1, col+1): environment[row+1, col+1] }
        


        if (all(x!=0 for x in surroundings.values())):
            # print("No Possible nodes to explore. I am stuck :(")
            continue
        for key, value in surroundings.items():
            if value == 0:
                # print("Valid Node found!")
                nodes_to_explore.append(key)
    
    return nodes_to_explore
    



def explore_node(location: tuple, environment):
    environment[location[0], location[1]] = color_value_for_path  # marks path with yellow (0.5 used for value)
    return environment


def explore_depth(starting_location: tuple, goal_location: tuple, environment, i): 
    current_locations = [starting_location]
    while True: 
        i += 1
        achieved = False
        # check our surroundings, get a list of eligible locations, change them all to yellow, 
        eligible_nodes = check_surroundings(environment = environment, current_locations= current_locations)
        if len(eligible_nodes) == 0:
            print("No Possible nodes to move to. I am stuck :(")
            break

        for node in eligible_nodes:
            new_env = explore_node(node, environment)
            environment = new_env
            current_location = node
            if current_location == goal_location:
                achieved = True
                break 
            else:
                environment, achieved, i = explore_depth(starting_location= current_location, goal_location=goal_location, environment= environment, i = i) #recursion
            
        else:
            # current_locations = eligible_nodes
         
            continue
        break
    return environment, achieved, i

def depth_first(starting_location: tuple, goal_location: tuple, environment):
    print("Beginning Depth First Search!")
    print(f"Goal Location: {goal_location}")
    i = 0

    new_env, achieved, i = explore_depth(starting_location=starting_location, goal_location= goal_location, environment= environment, i = i)
    if achieved:
        print("Goal location has been achieved!")
    environment[goal_location[0], goal_location[1]] = np.nan
    environment[starting_location[0], starting_location[1]] = color_value_for_path
    return new_env, i


def breadth_first(starting_location: tuple, goal_location: tuple, environment): 
    print("Beginning Breadth First Search!")
    print(f"Goal Location: {goal_location}")
    current_locations = [starting_location]
    i = 0
    while True: 
        i += 1
        achieved = False
        # check our surroundings, get a list of eligible locations, change them all to yellow, 
        eligible_nodes = check_surroundings(environment = environment, current_locations= current_locations)
        if len(eligible_nodes) == 0:
            print("No Possible nodes to move to. I am stuck :(")
            new_env = environment
            break
        for node in eligible_nodes:
            new_env = explore_node(node, environment)
            environment = new_env
            current_location = node
            if current_location == goal_location:
                achieved = True
                break
        else:
            current_locations = eligible_nodes
            # print(current_locations)
            continue
        break
    
    if achieved:
        print("Goal location has been achieved!")
    environment[goal_location[0], goal_location[1]] = np.nan
    environment[starting_location[0], starting_location[1]] = color_value_for_path

    return new_env, i


def create_bordered_env(coverage, grid_size):

    init_env = np.zeros((grid_size, grid_size))

    # Adding the borders
    init_env[0, 0:grid_size], init_env[1:grid_size-1, 0], init_env[1:(grid_size-1), (grid_size-1)], init_env[(grid_size-1), 0:grid_size] = 1,1,1,1


    # Generating the obstacles within the area NOT including the border
    obstacle_field, coverage = create_obstacle_field(np.zeros(((grid_size-2),(grid_size-2))), goal_coverage= coverage)  # NOTE that size of environment given to create_obstacle_field is only the area that doesn't include the border from the init_env

    # Adding the obstacles to the initial environment
    init_env[1:(grid_size-1), 1:(grid_size-1)] = obstacle_field

    return init_env

if __name__ == "__main__":

# ------------------ Getting Static Plots ----------------------------------------  
    # import os

    # env_0 = create_bordered_env(coverage=0, grid_size=128)
    # env_25 = create_bordered_env(coverage=0.25, grid_size=128)
    # env_50 = create_bordered_env(coverage=0.5, grid_size=128)
    # env_65 = create_bordered_env(coverage=0.65, grid_size=128)

    starting_row, starting_col, init_env = place_robot("NW", init_env)

    # Displaying the environment


    # os.chdir(r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_2")
    # np.save("0_coverage.npy", env_0)
    # np.save("25_coverage.npy", env_25)
    # np.save("50_coverage.npy", env_50)
    # np.save("65_coverage.npy", env_65)

    # cmap = ListedColormap(["white", "blue", "black"]) # sets 0 as white, 1 as black. See https://stackoverflow.com/questions/68390704/assign-specific-colors-to-values-of-an-array-when-plotting-it-using-imshow-witho
    # cmap.set_bad("red")   # sets value that's not 0 or 1 to red. In this case it's np.nan. 

    # plt.subplot(2, 4, (1,5)), plt.imshow(env_0, cmap =  cmap), plt.title("0% Coverage")
    # plt.subplot(2, 4, (2,6)), plt.imshow(env_25, cmap = cmap), plt.title("25% Coverage")
    # plt.subplot(2, 4, (3,7)), plt.imshow(env_50, cmap = cmap), plt.title("50% Coverage")
    # plt.subplot(2, 4, (4,8)), plt.imshow(env_65, cmap = cmap), plt.title("65% Coverage")

    # # plt.imshow(breadth_env_25, cmap=cmap)
    # plt.show()


# ----------------------------------------------------------


    np.set_printoptions(threshold=sys.maxsize)


    # Initial Environment with Closed Border
    grid_size = 128
    color_value_for_path = 0.5
    path = r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_2"


    #  ---------------------------------     Performing Breadth First Search -------------------------------------------------------------

    goal_location = (25,25)

    """
    0% Coverage Calculations
    """
    start_env = np.load(path + "/0_coverage.npy")
    print(f"Coverage = 0%")
    starting_row, starting_col, init_env = place_robot("NW", start_env)
    starting_location = (starting_row, starting_col)
    init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a cleared goal area

    breadth_env_0, iterations_breadth_0 = breadth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
    print(f"Number of Iterations: {iterations_breadth_0}\n")

    """
    25% Coverage Calculations
    """
    start_env = np.load(path + "/25_coverage.npy")
    print(f"Coverage = 25%")
    starting_row, starting_col, init_env = place_robot("NW", start_env)
    starting_location = (starting_row, starting_col)
    init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a cleared goal area

    breadth_env_25, iterations_breadth_25 = breadth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
    print(f"Number of Iterations: {iterations_breadth_25}\n")

    """
    50% Coverage Calculations
    """
    start_env = np.load(path + "/50_coverage.npy")
    print(f"Coverage = 50%")
    starting_row, starting_col, init_env = place_robot("NW", start_env)
    starting_location = (starting_row, starting_col)
    init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a cleared goal area

    breadth_env_50, iterations_breadth_50 = breadth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
    print(f"Number of Iterations: {iterations_breadth_50}\n")
    """
    75% Coverage Calculations
    """

    start_env = np.load(path + "/65_coverage.npy")
    print(f"Coverage = 65%")
    starting_row, starting_col, init_env = place_robot("NW", start_env)
    starting_location = (starting_row, starting_col)
    init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a cleared goal area

    breadth_env_75, iterations_breadth_75 = breadth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
    print(f"Number of Iterations: {iterations_breadth_75}\n")


    #  ---------------------------------     Performing Depth First Search -------------------------------------------------------------

    """
    0% Coverage Calculations
    """
    # start_env = create_bordered_env(coverage= 0, grid_size=grid_size)
    # starting_row, starting_col, init_env = place_robot("NW", start_env)
    # starting_location = (starting_row, starting_col)
    # init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

    # depth_env_0, iterations_breadth_0 = depth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
    # print(f"Number of Iterations: {iterations_depth_0}\n")

    """
    25% Coverage Calculations
    """
    # start_env = create_bordered_env(coverage= 0.25, grid_size=grid_size)
    # starting_row, starting_col, init_env = place_robot("NW", start_env)
    # starting_location = (starting_row, starting_col)
    # init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

    # depth_env_25, iterations_breadth_25 = depth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
    # print(f"Number of Iterations: {iterations_depth_25}\n")

    """
    50% Coverage Calculations
    """
    # start_env = create_bordered_env(coverage= 0.250, grid_size=grid_size)
    # starting_row, starting_col, init_env = place_robot("NW", start_env)
    # starting_location = (starting_row, starting_col)
    # init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

    # depth_env_50, iterations_breadth_50 = depth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
    # print(f"Number of Iterations: {iterations_depth_50}\n")
    """
    75% Coverage Calculations
    """

    # start_env = create_bordered_env(coverage= 0.70, grid_size=grid_size)
    # starting_row, starting_col, init_env = place_robot("NW", start_env)
    # starting_location = (starting_row, starting_col)
    # init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

    # depth_env_75, iterations_breadth_75 = depth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
    # print(f"Number of Iterations: {iterations_depth_75}\n")

    # ---------------------------------     Plots         -------------------------------------------------------------

    plt.figure("Assignment 2: Flatland Assignment")
    plt.suptitle(f"Breadth First Search - Goal Location: {goal_location}")
    cmap = ListedColormap(["white", "blue", "black"]) # sets 0 as white, 1 as black. See https://stackoverflow.com/questions/68390704/assign-specific-colors-to-values-of-an-array-when-plotting-it-using-imshow-witho
    cmap.set_bad("red")   # sets value that's not 0 or 1 to red. In this case it's np.nan. 

    plt.subplot(2, 4, (1,5)), plt.imshow(breadth_env_0, cmap =  cmap), plt.title("0% Coverage")
    plt.subplot(2, 4, (2,6)), plt.imshow(breadth_env_25, cmap = cmap), plt.title("25% Coverage")
    plt.subplot(2, 4, (3,7)), plt.imshow(breadth_env_50, cmap = cmap), plt.title("50% Coverage")
    plt.subplot(2, 4, (4,8)), plt.imshow(breadth_env_75, cmap = cmap), plt.title("65% Coverage")

    # plt.imshow(breadth_env_25, cmap=cmap)


    plt.show()