import numpy as np
from matplotlib import pyplot as plt
import random

def add_tetromino(environment): 

    random_row = random.randint(3, environment.shape[0]-3)  # must be a 3 block perimeter to insert tetromino without exceeding array size
    random_col = random.randint(3, environment.shape[1]-3)
    random_tetromino = tetrominoes[random.randint(0, len(tetrominoes)-1)]
    tetromino_height = random_tetromino.shape[0]
    tetromino_width = random_tetromino.shape[1]

    # environment[random_row : random_row + tetromino_height][random_col : random_col + tetromino_width] = random_tetromino
    environment[random_row : (random_row + tetromino_height), random_col : (random_col + tetromino_width)] = random_tetromino
    return environment

def check_coverage(environment): 
    occurrence_count = np.count_nonzero(environment)
    coverage = occurrence_count/(environment.size)
    return coverage

def show_obstacle_field(environment):
    plt.imshow(environment, cmap = "binary")
    plt.show()



def create_obstacle_field(environment, goal):
    coverage = 0
    while coverage < goal: 
        new_env = add_tetromino(environment)
        coverage = check_coverage(new_env)
    return new_env, coverage

if __name__ == "__main__": 
    tetrominoes = [np.ones((4,1)), 
               np.array([[1,1],[0,1],[0,1]]), 
               np.array([[1,0],[1,1],[0,1]]),
               np.array([[0,1],[1,1],[0,1]])]

    grid_size = 128

    env = np.zeros((grid_size, grid_size))

    obstacle_field_1, coverage_1 = create_obstacle_field(env, goal = 0.1)
    # obstacle_field_1, coverage_2 = create_obstacle_field(env, goal = 0.5)
    # obstacle_field_3, coverage_3 = create_obstacle_field(env, goal = 0.7)

    plt.subplot(1, 3, (1)), plt.imshow(obstacle_field_1, cmap = "binary"), plt.title(f"{round(coverage_1 * 100)} % Coverage")
    # plt.subplot(1, 3, (2)), plt.imshow(obstacle_field_2, cmap = "binary"), plt.title(f"{round(coverage_2 * 100)} % Coverage")
    # plt.subplot(1, 3, (3)), plt.imshow(obstacle_field_3, cmap = "binary"), plt.title(f"{round(coverage_3* 100)} % Coverage")
    plt.suptitle("Obstacle Fields")

    plt.show()
