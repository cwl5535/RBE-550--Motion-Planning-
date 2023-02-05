from obstacle_field import create_obstacle_field
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import sys

np.set_printoptions(threshold=sys.maxsize)


# Initial Environment with Closed Border
grid_size = 128

init_env = np.zeros((grid_size, grid_size))

# Adding the borders
init_env[0, 0:grid_size], init_env[1:grid_size-1, 0], init_env[1:(grid_size-1), (grid_size-1)], init_env[(grid_size-1), 0:grid_size] = 1,1,1,1

# Generating the obstacles within the area NOT including the border
obstacle_field, coverage = create_obstacle_field(np.zeros(((grid_size-2),(grid_size-2))), goal_coverage= 0.25)  # NOTE that size of environment given to create_obstacle_field is only the area that doesn't include the border from the init_env

# Adding the obstacles to the initial environment
init_env[1:(grid_size-1), 1:(grid_size-1)] = obstacle_field

def collision_check(direction): 
    if direction == "W": 
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
    
    return row, col


if __name__ == "__main__":
    starting_row, starting_col = place_robot("NW", init_env)

    init_env[starting_row, starting_col] = np.nan  # making the robot a value that isn't 0 or 1 for a different color
    # Displaying the environment

    plt.figure("Assignment 2: Flatland Assignment")


    cmap = ListedColormap(["white", "black"]) # sets 0 as white, 1 as black. See https://stackoverflow.com/questions/68390704/assign-specific-colors-to-values-of-an-array-when-plotting-it-using-imshow-witho
    cmap.set_bad("red")   # sets value that's not 0 or 1 to red. In this case it's np.nan. 

    plt.imshow(init_env, cmap=cmap)


    plt.show()