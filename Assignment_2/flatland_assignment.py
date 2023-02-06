from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import sys

"""
Author: Colton Layhue
Assignment 2 - RBE 550 Motion Planning - Forward Search Planners
Worcester Polytechnic Institute
Spring 2023
"""

def place_robot(starting_quadrant: str, obstacle_field):
    """"
    Purpose: This function finds an open spot in a given obstacle field to place the poitn robot. The location is based on the quadrant given to the function northwest (NW), northeast (NE), southwest (SW), or southeast (SE).
    
    Arguments: 
        starting_quadrant: `string` - Quadrant to place robot in. Options include NW, NE, SW, SE
        obstacle_field: `numpy array` - obstacle field to place robot in. 
    """
    
    obs_field_height = obstacle_field.shape[0]
    obs_field_width = obstacle_field.shape[1]


    # cutting the environment up into 4 quadrants
    # TODO: Fix other 3 quadrants

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


def check_surroundings_random_search(environment, current_locations) -> list:
    """
    Purpose: To check the nodes in each of the 4 cardinal directions from the current node, Random Search Specific
    
    This function checks which nodes are available to be explored and appends it to a list of eligible nodes to explore. This list of eligible nodes is check with this same function. 
   

    Returns: `nodes_to_explore`: `list` - list of `tuples` to be explored by the robot.  
    """
    nodes_to_explore = []
    row = current_locations[0]
    col = current_locations[1] 

    # surroundings = {(row-1, col-1): environment[row-1, col-1],    (row-1, col): environment[row-1, col],     (row-1, col+1): environment[row-1, col+1],
    #                 (row,   col-1): environment[row,   col-1],                                               (row,   col+1): environment[row,   col+1], 
    #                 (row+1, col-1): environment[row+1, col-1],    (row+1, col): environment[row+1, col],     (row+1, col+1): environment[row+1, col+1] }
    
    surroundings = {                                          (row-1, col): environment[row-1, col],
                    (row,   col-1): environment[row,   col-1],                                               (row,   col+1): environment[row,   col+1], 
                                                                (row+1, col+1): environment[row+1, col+1] }
    


    if (all(x!=0 for x in surroundings.values())):  # if all surrounding values have either been explored or are a wall, 
        # print("No Possible nodes to explore. I am stuck :(")
        return nodes_to_explore
    for key, value in surroundings.items():
        if value == 0:
            # print("Valid Node found!")
            nodes_to_explore.append(key)

    return nodes_to_explore

def check_surroundings_BFS(environment, current_locations: list) -> list:
    """
    Purpose: To check the nodes in each of the 4 cardinal directions from the current node, Breadth First Search Specific
    
    This function checks which nodes are available to be explored and appends it to a list of eligible nodes to explore. This list of eligible nodes is check with this same function. 
    Note: This breadth first specific function can handle a list of current locations, since breadth first will examine all notes at the same level before expanding. 

    Returns: `nodes_to_explore`: `list` - list of `tuples` to be explored by the robot.  
    """
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
        


        if (all(x!=0 for x in surroundings.values())):  # if all surrounding values have either been explored or are a wall, do not append any values to the nodes_to_explore list
            # print("No Possible nodes to explore. I am stuck :(")
            continue
        for key, value in surroundings.items():
            if value == 0:
                # print("Valid Node found!")
                nodes_to_explore.append(key)
    
    return nodes_to_explore

def check_surroundings_DFS(environment, current_location: tuple, stack) -> list:
    """
    Purpose: To check the nodes in each of the 4 cardinal directions from the current node, Depth First Search Specific
    DFS only does one node at a time
    Checks what nodes are available to be explored and adds it to the stack
    """

    row = current_location[0]
    col = current_location[1] 

    # surroundings = {(row-1, col-1): environment[row-1, col-1],    (row-1, col): environment[row-1, col],     (row-1, col+1): environment[row-1, col+1],
    #                 (row,   col-1): environment[row,   col-1],                                               (row,   col+1): environment[row,   col+1], 
    #                 (row+1, col-1): environment[row+1, col-1],    (row+1, col): environment[row+1, col],     (row+1, col+1): environment[row+1, col+1] }
    
    surroundings = {                                          (row-1, col): environment[row-1, col],
                    (row,   col-1): environment[row,   col-1],                                               (row,   col+1): environment[row,   col+1], 
                                                                (row+1, col+1): environment[row+1, col+1] }
    


    if (all(x!=0 for x in surroundings.values())):  # if all surrounding values have either been explored or are a wall, 
        # print("No Possible nodes to explore. I am stuck :(")
        return stack
    else:
        for key, value in surroundings.items():
            if value == 0:
            # print("Valid Node found!")
                stack.append(key)
        return stack


def explore_node(location: tuple, environment):
    """
    Purpose: function to enter node location and mark it as explored by changing its color and value to yellow and 0.5

    Arugments: 
        location: `tuple` - node coordinate to explore
        environment: `np arrray` - obstacle field where node is located

    Returns: 
        environment: `np array` - updated obstacle field with node now marked as traveled upon
    """
    environment[location[0], location[1]] = color_value_for_path  # marks path with yellow (0.5 used for value)
    return environment


def explore_depth(starting_location: tuple, goal_location: tuple, environment, i: int, stack: list): 
    """
    Purpose: Separate explore function to enable recursion for Depth First Search. 

    Description: 
        This function utilizes the `check_surroundings_DFS` function to identify which nodes are able to be explored and then moves the robot to that point. After a node is explored, the next node is popped from the stack and explored. 
        There are checks within the loops to see if the robot has achieved its goal, whether there are no points left to explore, and to handle any recursion errors. The recursion limit can be changed in the user input section. 

    Arguments: 
        starting_location: `tuple` - coordinates of where the robot is placed using `place_robot` function
        goal_location: `tuple` - coordinates of where the robot should end
        environment: `numpy array` - desired array or obstacle field for the robot to explore
        i: `int` - used for keeping track of the number of interations needed
        stack: `list` - list used to store a stack of what nodes to explore next. This enables the Last In, First Out of Depth first search
    
    Returns: 
        environment: 
        achieved: `bool` - Whether or not the robot reached its goal
        i: `int` - number of iterations needed
    """
    current_location = starting_location
    while True: 
        i += 1
        achieved = False
        # check our surroundings, get a list of eligible locations, change them all to yellow, 
        node_stack = check_surroundings_DFS(environment = environment, current_location= current_location, stack= stack)
        if len(node_stack) == 0:
            # print("No Possible nodes to move to. I am stuck :(")
            break
        last_node = node_stack.pop()
        new_env = explore_node(last_node, environment)
        environment = new_env
        current_location = last_node
        if current_location == goal_location:
            achieved = True
            break 
        else:
            try:
                environment, achieved, i = explore_depth(starting_location= current_location, goal_location=goal_location, environment= environment, i = i, stack= node_stack) #recursion
                break
            except RecursionError:
            #     # print("You have reached the recursion limit!")
                break
    return environment, achieved, i

def depth_first(starting_location: tuple, goal_location: tuple, environment):
    """
    Purpose: wrapper function for depth first search. This is the MAIN function to run to perform a depth first search. 
    """
    print("Beginning Depth First Search!")
    print(f"Goal Location: {goal_location}")
    i = 0
    stack = []
    new_env, achieved, i = explore_depth(starting_location=starting_location, goal_location= goal_location, environment= environment, i = i, stack= stack)
        
    if achieved:
        print("Goal location has been achieved!")
    environment[goal_location[0], goal_location[1]] = np.nan
    environment[starting_location[0], starting_location[1]] = color_value_for_path
    return new_env, i


def breadth_first(starting_location: tuple, goal_location: tuple, environment): 
    """
    Purpose: Main function to run breath first search. 
    Description: This function uses `check_surroundings_BFS` to identify nodes to move to, and cycles through them at each level. If all the nodes at a given level are explorerd, the remaining eligible nodes are assigned as the `current_locations` in the else loop so they can be run through the algorithm. 
    Once there are no more possible nodes to move to, the algorithm will end. 
    """
    print("Beginning Breadth First Search!")
    print(f"Goal Location: {goal_location}")
    current_locations = [starting_location]
    i = 0
    while True: 
        i += 1
        achieved = False
        # check our surroundings, get a list of eligible locations, change them all to yellow, 
        eligible_nodes = check_surroundings_BFS(environment = environment, current_locations= current_locations)
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
    

def random_search(starting_location: tuple, goal_location: tuple, environment):
    """
    Purpose: Main function to run random search. 
    Description: This function uses `check_surroundings_random_search` to identify nodes to move to, and moves to the first one available. 
    """

    print("Beginning Random Search!")
    print(f"Goal Location: {goal_location}")
    current_location = starting_location
    i = 0
    while True:
        i += 1
        achieved = False
        if i > 250:
            break
        eligible_nodes = check_surroundings_random_search(environment = environment, current_locations= current_location)
        if len(eligible_nodes) == 0: 
            print("No Possible nodes to move to. I am stuck :(")
            new_env = environment
            break
        for node in eligible_nodes: 
            if environment[node[0], node[1]] == 0: 
                new_env = explore_node(node, environment= environment)
                current_location = node
                if current_location == goal_location: 
                    achieved = True
                    break
    if achieved:
        print("Goal location has been achieved!")
    environment[goal_location[0], goal_location[1]] = np.nan
    environment[starting_location[0], starting_location[1]] = color_value_for_path

    return new_env, i

def dijkstras(starting_location: tuple, goal_location: tuple, environment):
    """
    Purpose: Main function to run dijkstras search. 
    Note: In this use case, the cost of each cell is assumed to be the same, causing the results to yield similar to Breadth First Search
    """
    
    print("Beginning Dijkstra's Search!")
    print(f"Goal Location: {goal_location}")
    current_locations = [starting_location]
    i = 0
    while True: 
        i += 1
        achieved = False
        # check our surroundings, get a list of eligible locations, change them all to yellow, 
        eligible_nodes = check_surroundings_BFS(environment = environment, current_locations= current_locations)
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
    """
    Purpose: Create a bordered obstacle field

    Arguments: 
        coverage: `float` - decimal between 0 and 1 to determine the level of coverage for the obstacle field i.e. 0.7 = 70% coverage
        grid_size: `int` - dimension of square grid to create
    """
    init_env = np.zeros((grid_size, grid_size))

    # Adding the borders
    init_env[0, 0:grid_size], init_env[1:grid_size-1, 0], init_env[1:(grid_size-1), (grid_size-1)], init_env[(grid_size-1), 0:grid_size] = 1,1,1,1


    # Generating the obstacles within the area NOT including the border
    obstacle_field, coverage = create_obstacle_field(np.zeros(((grid_size-2),(grid_size-2))), goal_coverage= coverage)  # NOTE that size of environment given to create_obstacle_field is only the area that doesn't include the border from the init_env

    # Adding the obstacles to the initial environment
    init_env[1:(grid_size-1), 1:(grid_size-1)] = obstacle_field

    return init_env

if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize)
    color_value_for_path = 0.5

# ----- User Inputs ------------

    grid_size = 128
    goal_location = (25,25)  # coordinate of goal
    test = "BFS"  # can be "static plots", "BFS", "DFS", "dijkstra", or "random"
    obstacle_file_location = r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_2"  # location of the npy files 


# ------------------ Getting Static Plots ----------------------------------------  
    if test == "static plots":
        import os

        env_0 = create_bordered_env(coverage=0, grid_size=128)
        env_25 = create_bordered_env(coverage=0.25, grid_size=128)
        env_50 = create_bordered_env(coverage=0.5, grid_size=128)
        env_65 = create_bordered_env(coverage=0.65, grid_size=128)

        starting_row, starting_col, init_env = place_robot("NW", init_env)

        # Displaying the environment


        os.chdir(r"C:\Users\layhu\Desktop\RBE-550--Motion-Planning-\Assignment_2")
        np.save("0_coverage.npy", env_0)
        np.save("25_coverage.npy", env_25)
        np.save("50_coverage.npy", env_50)
        np.save("65_coverage.npy", env_65)

        cmap = ListedColormap(["white", "blue", "black"]) # sets 0 as white, 1 as black. See https://stackoverflow.com/questions/68390704/assign-specific-colors-to-values-of-an-array-when-plotting-it-using-imshow-witho
        cmap.set_bad("red")   # sets value that's not 0 or 1 to red. In this case it's np.nan. 

        plt.subplot(2, 4, (1,5)), plt.imshow(env_0, cmap =  cmap), plt.title("0% Coverage")
        plt.subplot(2, 4, (2,6)), plt.imshow(env_25, cmap = cmap), plt.title("25% Coverage")
        plt.subplot(2, 4, (3,7)), plt.imshow(env_50, cmap = cmap), plt.title("50% Coverage")
        plt.subplot(2, 4, (4,8)), plt.imshow(env_65, cmap = cmap), plt.title("65% Coverage")

        # plt.imshow(breadth_env_25, cmap=cmap)
        plt.show()
# ----------------------------------------------------------
    #  ---------------------------------     Performing Breadth First Search -------------------------------------------------------------
    if test == "BFS":

        # """
        # 0% Coverage Calculations
        # """
        start_env = np.load(obstacle_file_location + "/0_coverage.npy")
        print(f"Coverage = 0%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a cleared goal area

        breadth_env_0, iterations_breadth_0 = breadth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_breadth_0}\n")

        # """
        # 25% Coverage Calculations
        # """
        start_env = np.load(obstacle_file_location + "/25_coverage.npy")
        print(f"Coverage = 25%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a cleared goal area

        breadth_env_25, iterations_breadth_25 = breadth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_breadth_25}\n")

        # """
        # 50% Coverage Calculations
        # """
        start_env = np.load(obstacle_file_location + "/50_coverage.npy")
        print(f"Coverage = 50%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a cleared goal area

        breadth_env_50, iterations_breadth_50 = breadth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_breadth_50}\n")
        # """
        # 65% Coverage Calculations
        # """

        start_env = np.load(obstacle_file_location + "/65_coverage.npy")
        print(f"Coverage = 65%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a cleared goal area

        breadth_env_65, iterations_breadth_65 = breadth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_breadth_65}\n")

        plt.figure("Assignment 2: Flatland Assignment")
        plt.suptitle(f"Depth First Search - Goal Location: {goal_location}")
        cmap = ListedColormap(["white", "blue", "black"]) # sets 0 as white, 1 as black. See https://stackoverflow.com/questions/68390704/assign-specific-colors-to-values-of-an-array-when-plotting-it-using-imshow-witho
        cmap.set_bad("red")   # sets value that's not 0 or 1 to red. In this case it's np.nan. 

        plt.subplot(2, 4, (1,5)), plt.imshow(breadth_env_0, cmap =  cmap), plt.title("0% Coverage")
        plt.subplot(2, 4, (2,6)), plt.imshow(breadth_env_25, cmap = cmap), plt.title("25% Coverage")
        plt.subplot(2, 4, (3,7)), plt.imshow(breadth_env_50, cmap = cmap), plt.title("50% Coverage")
        plt.subplot(2, 4, (4,8)), plt.imshow(breadth_env_65, cmap = cmap), plt.title("65% Coverage")


        plt.show()
    #  ---------------------------------     Performing Depth First Search -------------------------------------------------------------

    """
    0% Coverage Calculations
    """

    if test == "DFS":
        sys.setrecursionlimit(3000)  # exceeding 3000 causes issues
        start_env = np.load(obstacle_file_location + "/0_coverage.npy")
        print(f"Coverage = 0%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        depth_env_0, iterations_depth_0 = depth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_depth_0}\n")

        """
        25% Coverage Calculations
        """
        start_env = np.load(obstacle_file_location + "/25_coverage.npy")
        print(f"Coverage = 25%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        depth_env_25, iterations_depth_25 = depth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_depth_25}\n")

        """
        50% Coverage Calculations
        """
        start_env = np.load(obstacle_file_location + "/50_coverage.npy")
        print(f"Coverage = 50%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        depth_env_50, iterations_depth_50 = depth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_depth_50}\n")

        """
        65% Coverage Calculations
        """

        start_env = np.load(obstacle_file_location + "/65_coverage.npy")
        print(f"Coverage = 65%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        depth_env_65, iterations_depth_65 = depth_first(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_depth_65}\n")

        # ---------------------------------     Plots         -------------------------------------------------------------

        plt.figure("Assignment 2: Flatland Assignment")
        plt.suptitle(f"Depth First Search - Goal Location: {goal_location}")
        cmap = ListedColormap(["white", "blue", "black"]) # sets 0 as white, 1 as black. See https://stackoverflow.com/questions/68390704/assign-specific-colors-to-values-of-an-array-when-plotting-it-using-imshow-witho
        cmap.set_bad("red")   # sets value that's not 0 or 1 to red. In this case it's np.nan. 

        plt.subplot(2, 4, (1,5)), plt.imshow(depth_env_0, cmap =  cmap), plt.title("0% Coverage")
        plt.subplot(2, 4, (2,6)), plt.imshow(depth_env_25, cmap = cmap), plt.title("25% Coverage")
        plt.subplot(2, 4, (3,7)), plt.imshow(depth_env_50, cmap = cmap), plt.title("50% Coverage")
        plt.subplot(2, 4, (4,8)), plt.imshow(depth_env_65, cmap = cmap), plt.title("65% Coverage")


        plt.show()


    #  ---------------------------------     Performing Dijkstra's Search -------------------------------------------------------------

    if test == "dijkstra":
        start_env = np.load(obstacle_file_location + "/0_coverage.npy")
        print(f"Coverage = 0%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        dijkstras_env_0, iterations_dijkstras_0 = dijkstras(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_dijkstras_0}\n")

        """
        25% Coverage Calculations
        """
        start_env = np.load(obstacle_file_location + "/25_coverage.npy")
        print(f"Coverage = 25%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        dijkstras_env_25, iterations_dijkstras_25 = dijkstras(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_dijkstras_25}\n")

        """
        50% Coverage Calculations
        """
        start_env = np.load(obstacle_file_location + "/50_coverage.npy")
        print(f"Coverage = 50%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        dijkstras_env_50, iterations_dijkstras_50 = dijkstras(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_dijkstras_50}\n")

        """
        65% Coverage Calculations
        """

        start_env = np.load(obstacle_file_location + "/65_coverage.npy")
        print(f"Coverage = 65%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        dijkstras_env_65, iterations_dijkstras_65 = dijkstras(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_dijkstras_65}\n")

        # ---------------------------------     Plots         -------------------------------------------------------------

        plt.figure("Assignment 2: Flatland Assignment")
        plt.suptitle(f"Dijkstra's Search - Goal Location: {goal_location}")
        cmap = ListedColormap(["white", "blue", "black"]) # sets 0 as white, 1 as black. See https://stackoverflow.com/questions/68390704/assign-specific-colors-to-values-of-an-array-when-plotting-it-using-imshow-witho
        cmap.set_bad("red")   # sets value that's not 0 or 1 to red. In this case it's np.nan. 

        plt.subplot(2, 4, (1,5)), plt.imshow(dijkstras_env_0, cmap =  cmap), plt.title("0% Coverage")
        plt.subplot(2, 4, (2,6)), plt.imshow(dijkstras_env_25, cmap = cmap), plt.title("25% Coverage")
        plt.subplot(2, 4, (3,7)), plt.imshow(dijkstras_env_50, cmap = cmap), plt.title("50% Coverage")
        plt.subplot(2, 4, (4,8)), plt.imshow(dijkstras_env_65, cmap = cmap), plt.title("65% Coverage")


        plt.show()

    #  ---------------------------------     Performing Random Search -------------------------------------------------------------

        """
    0% Coverage Calculations
    """
    if test == "random":
        start_env = np.load(obstacle_file_location + "/0_coverage.npy")
        print(f"Coverage = 0%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        random_env_0, iterations_random_0 = random_search(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_random_0}\n")

        """
        25% Coverage Calculations
        """
        start_env = np.load(obstacle_file_location + "/25_coverage.npy")
        print(f"Coverage = 25%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        random_env_25, iterations_random_25 = random_search(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_random_25}\n")

        """
        50% Coverage Calculations
        """
        start_env = np.load(obstacle_file_location + "/50_coverage.npy")
        print(f"Coverage = 50%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        random_env_50, iterations_random_50 = random_search(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_random_50}\n")

        """
        65% Coverage Calculations
        """

        start_env = np.load(obstacle_file_location + "/65_coverage.npy")
        print(f"Coverage = 65%")
        starting_row, starting_col, init_env = place_robot("NW", start_env)
        starting_location = (starting_row, starting_col)
        init_env[goal_location[0]-1: goal_location[0]+1, goal_location[1]-1: goal_location[1]+1] = 0  # create a goal area

        random_env_65, iterations_random_65 = random_search(starting_location=starting_location, goal_location=goal_location, environment=init_env)
        print(f"Number of Iterations: {iterations_random_65}\n")

        # ---------------------------------     Plots         -------------------------------------------------------------

        plt.figure("Assignment 2: Flatland Assignment")
        plt.suptitle(f"Random Search, 250 Iterations - Goal Location: {goal_location}")
        cmap = ListedColormap(["white", "blue", "black"]) # sets 0 as white, 1 as black. See https://stackoverflow.com/questions/68390704/assign-specific-colors-to-values-of-an-array-when-plotting-it-using-imshow-witho
        cmap.set_bad("red")   # sets value that's not 0 or 1 to red. In this case it's np.nan. 

        plt.subplot(2, 4, (1,5)), plt.imshow(random_env_0, cmap =  cmap), plt.title("0% Coverage")
        plt.subplot(2, 4, (2,6)), plt.imshow(random_env_25, cmap = cmap), plt.title("25% Coverage")
        plt.subplot(2, 4, (3,7)), plt.imshow(random_env_50, cmap = cmap), plt.title("50% Coverage")
        plt.subplot(2, 4, (4,8)), plt.imshow(random_env_65, cmap = cmap), plt.title("65% Coverage")


        plt.show()