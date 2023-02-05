from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import sys

def collision_check(cell_value): 
    if (cell_value == 1) or (cell_value == color_value_for_path):
        return True
def move():
    pass

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




class Robot(object): 
    def __init__(self, starting_location: tuple): 
        self.starting_location = starting_location  # tuple
        self.previous_location = None

def check_surroundings(environment, current_locations: list) -> list:
    nodes_to_explore = []
    # surroundings = environment[row-1: col-1 , row+1 : col+1]

    surroundings = {(row-1, col-1): environment[row-1, col-1],    (row-1, col): environment[row-1, col],     (row-1, col+1): environment[row-1, col+1],
                    (row,   col-1): environment[row,   col-1],                                               (row,   col+1): environment[row,   col+1], 
                    (row+1, col-1): environment[row+1, col-1],    (row+1, col): environment[row+1, col],     (row+1, col+1): environment[row+1, col+1] }

    for key, value in surroundings.items():
        if value == 0:
            nodes_to_explore.append(key)
    
    # environment[(row-1):(col-1), (row+1):(col+1)] = surroundings

    # updated_env = environment
    return nodes_to_explore
    



def explore_cell(location: tuple, environment):
    environment[location[0], location[1]] = color_value_for_path
    return environment


def breadth_first(starting_location: tuple, goal_location: tuple, environment): 
    print("Beginning Breadth First Search")
    current_location = starting_location
    while True: 
        # check our surroundings, get a list of eligible locations, change them all to yellow, 
        eligible_nodes = check_surroundings(environment = environment, current_location= current_location)
        for node in eligible_nodes:
            new_env = explore_cell(node, environment)
            environment = new_env
            current_location = node
            if current_location == goal_location:
                break
        else:
            continue
        break
    
    print("Goal location has been achieved!")
    # environment[goal_location[0], goal_location[1]] = np.nan
    # environment[starting_location[0], starting_location[1]] = color_value_for_path
    return new_env
if __name__ == "__main__":

    np.set_printoptions(threshold=sys.maxsize)


    # Initial Environment with Closed Border
    grid_size = 128
    color_value_for_path = 0.5
    init_env = np.zeros((grid_size, grid_size))

    # Adding the borders
    init_env[0, 0:grid_size], init_env[1:grid_size-1, 0], init_env[1:(grid_size-1), (grid_size-1)], init_env[(grid_size-1), 0:grid_size] = 1,1,1,1

    # Generating the obstacles within the area NOT including the border
    obstacle_field, coverage = create_obstacle_field(np.zeros(((grid_size-2),(grid_size-2))), goal_coverage= 0.05)  # NOTE that size of environment given to create_obstacle_field is only the area that doesn't include the border from the init_env

    # Adding the obstacles to the initial environment
    init_env[1:(grid_size-1), 1:(grid_size-1)] = obstacle_field


    # Placing the Robot
    starting_row, starting_col, init_env = place_robot("NW", init_env)

    # Performing Breadth First Search
    goal_location = (120, 120)
    init_env[goal_location[0], goal_location[1]] = 0  # create a goal area
    final_env = breadth_first((starting_row, starting_col), goal_location=goal_location, environment=init_env)








    # Displaying the environment

    plt.figure("Assignment 2: Flatland Assignment")


    cmap = ListedColormap(["white", "yellow", "black"]) # sets 0 as white, 1 as black. See https://stackoverflow.com/questions/68390704/assign-specific-colors-to-values-of-an-array-when-plotting-it-using-imshow-witho
    cmap.set_bad("red")   # sets value that's not 0 or 1 to red. In this case it's np.nan. 

    plt.imshow(final_env, cmap=cmap)


    plt.show()