from math import sqrt, pi, inf, radians, cos, sin
from typing import List, Tuple
from matplotlib import pyplot as plt
import numpy as np
import time
from geometry import Point
from world import World
from agents import Car, RectangleBuilding
from create_world import create_world

# create world with obstacles >> have a way to access the x and y of obstacles



class State():
    def __init__(self, x = 0, y = 0, theta = 0, velocity = Point(0,0), f = inf): 

        #self.cost_to_go = self.distance_to_goal(goal) # going to be calculated with Euclidean formulas 
        self.g = 0
        self.h = 0
        self.f = f
        self.x = x
        self.y = y
        self.theta = theta # possible states are 0 to 2pi, in 15 degree intervals
        self.parent = None
        self.velocity = velocity

    def distance_to(self, to) -> float:
        if isinstance(to, tuple):
            delta_x = self.x - to[0]
            delta_y = self.x - to[1]
        else:
            delta_x = self.x - to.x
            delta_y = self.y - to.y
        dist = sqrt((delta_x**2) + (delta_y**2))
        return dist
    
    def calculate_g(self, parent) -> float:
        # Distance Cost 

        distance = self.distance_to(parent)
        dist_cost = parent.g + distance

        # Steering Cost

        steering_cost = abs(self.theta - parent.theta)

        total_cost = dist_cost + steering_cost

        # total_cost = round(dist_cost + steering_cost,2)

        return total_cost

    def calculate_h(self, goal):
        return self.distance_to(goal)
    
    def calculate_f(self):
        return self.g + self.h
    

class AStar():
    def __init__(self, car, obstacles_x, obstacles_y, world, start: tuple, goal: tuple):

        self.start = State(start[0], start[1], start[2], f = 0)  # start should be a 3 element tuple, with x y and theta values
        self.goal = goal
        self.path = [State(start[0], start[1], start[2], f = 0)]
        self.car = car
        self.obstacles_x: List[Tuple] = obstacles_x
        self.obstacles_y: List[Tuple] = obstacles_y
        self.world = world
        
    def add_to_open(self, state):
        self.open.append(state)

    def add_to_closed(self, state):
        self.closed.append(state)

    def simulate(self, current_state, car, world):
        car.velocity = current_state.velocity
        # print(self.car.velocity)
        car.inputSteering = current_state.theta
        world.tick()
        world.render()
        time.sleep(0.1/4)
    
    def show_path(self, last_state):
        path = np.zeros((120,120))
        state_to_plot = last_state
        while state_to_plot != self.start:
            x = state_to_plot.x
            y = state_to_plot.y
            path[x][y] = 1
            state_to_plot = state_to_plot.parent
        path[self.start.x][self.start.y] = 1
            # need to take the current one, make the value at its x,y a one, and then do the same for its parent and their parents

        plt.figure("Assignment 3 (RBE 550): Valet")
        plt.imshow(path, cmap = "binary")

        plt.show()
    def collision_check(self, state) -> bool:
        
        for index in range(len(self.obstacles_x)):
            x_left = self.obstacles_x[index][0]  # indexing a tuple 
            x_right= self.obstacles_x[index][1]
            y_left = self.obstacles_y[index][0]
            y_right= self.obstacles_y[index][1]

            if (round(state.x) in range(x_left, x_right+1)) and (round(state.y) in range(y_left, y_right + 1)):
                self.add_to_closed(state)  # state causes collision and is added to closed as a result
                print("Collision Occurred")
                return True
        return False
    def plan(self):
        self.start.h = self.start.calculate_h(self.goal)
        self.start.f = self.start.calculate_f()

        # self.add_to_open(self.start)
        self.open = []
        self.closed = []

        self.add_to_open(self.start)


        q = self.start

        goal_found = False
        idx = 0
        # test 
        while len(self.open) > 0 and (not goal_found):
            idx += 1 
            if idx == 5000: 
                self.show_path(q)
                break
            print(f"x: {q.x}, y: {q.y}, theta: {q.theta}")
            # print(f"Open list has {len(self.open)} states")

            # current = self.open[0]
            self.simulate(q, self.car, self.world)
            self.open.pop(self.open.index(q))
            self.add_to_closed(q)
            # search for the surrounding neighbors
 
            neighbors = self.get_neighbors(q, timestep=0.5)

            previous_f = neighbors[0].f

            for neighbor in neighbors:
                if neighbor not in self.closed:
                        
                    if self.goal_check(neighbor):
                        print("Goal found")
                        self.show_path(q)
                        break
                    
                    else:
                        neighbor.g = neighbor.calculate_g(neighbor.parent)
                        neighbor.h = neighbor.calculate_h(self.goal)
                        neighbor.f = neighbor.calculate_f()
                    
                    if neighbor.f < previous_f:
                        q = neighbor
                        previous_f = neighbor.f
                
            self.add_to_open(q)



            # for neighbor in neighbors: 
            #     if neighbor not in self.closed:
                    
                    
            #         if self.collision_check(neighbor):
            #             continue
            #         tentative_g = current.calculate_g(neighbor)

            #         if tentative_g < neighbor.g:
            #             neighbor.g = tentative_g
            #             neighbor.parent = current
            #             neighbor.h = neighbor.calculate_h(self.goal)
            #             neighbor.f = neighbor.calculate_f()
            #             self.add_to_open(neighbor)
            


    def refine_c_space(self, state: State, obstacle_location): # function to avoid creation of states where obstacles exist
        if (state.x in obstacle_location.x) or (state.y in obstacle_location.y):
            self.add_to_closed(state)
    
    def goal_check(self, state: State):
        current_state = (state.x, state.y, state.theta) 

        if current_state == self.goal: 
            return True
        
        return False

    def get_neighbors(self, state, timestep = 0.1) -> List[State]:
        if isinstance(state, State):
            neighbors = []

            # what are all possible options to go to? I need to vary my position (x,y, theta) with the velocity equations
            # my inputs are for lecture 10, slide 26 is vl and vr. Combinations of each wheel's velocities
            
            R = 0.1
            L = 0.4
            max_speed = 5

            speeds = []

            for speed in range(1, max_speed+1): # looping to get all possible speed combos for the two wheels
                speeds.append((speed, max_speed))
                speeds.append((max_speed, speed))
            
            speeds.sort()
            
            for speed in speeds: 
                # calculating velocity and position with each speed combo
                vr, vl = speed[0], speed[1]
                            
                theta_dot = (R/L)*(vr - vl)
                theta =  state.theta + (theta_dot*timestep) 

                x_dot = (R/2)*(vr + vl)*cos(theta)
                x = state.x + (x_dot * timestep)
                

                y_dot = (R/2)*(vr + vl)*sin(theta)
                y = state.y + (y_dot * timestep)

                print(x_dot, y_dot, theta_dot)
                neighbor_state = State(x, y, theta, velocity= Point(x_dot, y_dot))
                neighbor_state.parent = state
                neighbors.append(neighbor_state)
            
            return neighbors
        else:
            return 0

# if __name__ == "__main__":
#     planner = AStar((0,0,0), (30, 35, 0))
#     planner.plan()
        


