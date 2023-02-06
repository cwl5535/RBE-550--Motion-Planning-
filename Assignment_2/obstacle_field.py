import numpy as np
from matplotlib import pyplot as plt
import random

"""
Author: Colton Layhue
Assignment 0 - RBE 550 Motion Planning - Create Obstacle Field
Worcester Polytechnic Institute
Spring 2023
"""

def add_tetromino(environment, tetrominoes): 
    '''
    Arguments: 
        environment - `numpy array`, environment to add obstacle to. 
    Description: function to add tetronimo to given environment
    '''

    # random number used to find a position in the environment to place tetromino
    random_row = random.randint(0, environment.shape[0])  
    random_col = random.randint(0, environment.shape[1])
    random_tetromino = tetrominoes[random.randint(0, len(tetrominoes)-1)]
    tetromino_height = random_tetromino.shape[0]
    tetromino_width = random_tetromino.shape[1]


    '''
    Different coordinates of where to place tetromino are given based on quadrant within obstacle field.
    Coordinates allow for all pieces, regardless of size, are able to be placed successfully. 
    '''
    if (random_row < (environment.shape[0]//2)) and (random_col < (environment.shape[1]//2)): # Quadrant 1
         environment[random_row : (random_row + tetromino_height), random_col : (random_col + tetromino_width)] = random_tetromino
    
    if (random_row < (environment.shape[0]//2)) and (random_col > (environment.shape[1]//2)): # Quadrant 2
        environment[random_row : (random_row + tetromino_height), (random_col - tetromino_width) : random_col] = random_tetromino
    
    if (random_row > (environment.shape[0]//2)) and (random_col < (environment.shape[1]//2)): # Quadrant 3
        environment[(random_row - tetromino_height) : random_row, random_col : (random_col + tetromino_width)] = random_tetromino
    
    if (random_row > (environment.shape[0]//2)) and (random_col > (environment.shape[1]//2)): # Quadrant 4
        environment[(random_row - tetromino_height) : random_row, (random_col - tetromino_width) : random_col] = random_tetromino

    return environment

def check_coverage(environment): 
    """
    Arguments: 
        environment - `numpy array`, environment that contains obstacles to be counted
    Description: Function to check overage coverage of tetrominos in a given environment. 
    Note: since only 1s or 0s are used, `np.count_nonzero` can be used to count the number of occupied spaces
    """
    occurrence_count = np.count_nonzero(environment)
    coverage = occurrence_count/(environment.size)
    return coverage

def show_obstacle_field(environment):
    '''
    Arguments: 
        environment - `numpy array`, desired environment to be shown
    Description: Function to show a given obstacle field
    '''
    plt.imshow(environment, cmap = "binary")
    plt.show()



def create_obstacle_field(environment, goal_coverage):

    """
    Arguments: 
        environment - `numpy array` , initial environment to create obstacle field onto. 
        goal_coverage - `float` , decimal value of desired coverage for obstacle field i.e. 0.7 means 70%. 
    Description: 
    """

    tetrominoes = [np.ones((4,1)), 
               np.array([[1,1],[0,1],[0,1]]), 
               np.array([[1,0],[1,1],[0,1]]),
               np.array([[0,1],[1,1],[0,1]])]

    coverage = 0

    if goal_coverage == 0:
        new_env = environment
        print(f"Coverage = 0%")
    else:
        new_env = add_tetromino(environment, tetrominoes)

        while coverage < goal_coverage: 
            new_env = add_tetromino(new_env, tetrominoes)
            coverage = check_coverage(new_env)
        cov_print = round(coverage * 100)

        print(f"Coverage = {cov_print}%")
    return new_env, coverage

if __name__ == "__main__": 
    tetrominoes = [np.ones((4,1)), 
               np.array([[1,1],[0,1],[0,1]]), 
               np.array([[1,0],[1,1],[0,1]]),
               np.array([[0,1],[1,1],[0,1]])]

    grid_size = 128


    obstacle_field_1, coverage_1 = create_obstacle_field(np.zeros((grid_size, grid_size)), goal_coverage = 0.1)
    obstacle_field_2, coverage_2 = create_obstacle_field(np.zeros((grid_size, grid_size)), goal_coverage = 0.5)
    obstacle_field_3, coverage_3 = create_obstacle_field(np.zeros((grid_size, grid_size)), goal_coverage = 0.7)

    plt.figure("Assignment 0 (RBE 550): Creating Obstacle Fields")
    plt.subplot(2, 3, (1,4)), plt.imshow(obstacle_field_1, cmap = "binary"), plt.title(f"{round(coverage_1 * 100)} % Coverage")
    plt.subplot(2, 3, (2,5)), plt.imshow(obstacle_field_2, cmap = "binary"), plt.title(f"{round(coverage_2 * 100)} % Coverage")
    plt.subplot(1, 3, (3)), plt.imshow(obstacle_field_3, cmap = "binary"), plt.title(f"{round(coverage_3* 100)} % Coverage")
    plt.suptitle("Obstacle Fields")
   

    plt.show()
