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
        self.theta = theta # has to be in radians
        self.position = (x, y)
        self.parent = None
        self.velocity = velocity

    def distance_to(self, to) -> float:
        # Used to calculate the Euclidean distance between one node to another
        if isinstance(to, tuple):
            delta_x = self.x - to[0]
            delta_y = self.y - to[1]
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

        steering_cost = 2*(abs(self.theta - parent.theta) % (2*pi))

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

    def simulate(self, path_x, path_y, path_theta):

        print("Beginning Simulation...")
        time.sleep(5.)
        
        for i in range(len(path_x)): 
            self.car.center = Point(path_x[i], path_y[i])
            self.car.heading = path_theta[i]
            self.world.tick()
            self.world.render()
            time.sleep(0.1/2)

        print("Holding Simulation for 10 seconds...")
        time.sleep(10.)
        self.world.close()
    
    def show_path(self, last_state):
        path_x = []
        path_y = []
        path_theta = []
        state_to_plot = last_state
        while state_to_plot != self.start:
            x = state_to_plot.x
            y = state_to_plot.y
            theta = state_to_plot.theta
            path_x.insert(0,x)
            path_y.insert(0,y)
            path_theta.insert(0,theta)
            state_to_plot = state_to_plot.parent
        path_x.insert(0,self.start.x)
        path_y.insert(0,self.start.y)
        path_theta.insert(0, self.start.theta)

        plt.plot(path_x, path_y, linewidth = 4)
        plt.plot(self.start.x, self.start.y, color = "red", marker = "o", markersize = 8)
        plt.plot(self.goal[0], self.goal[1], color = "green", marker = "o", markersize = 8)
        plt.legend(["Path", "Start", "Goal"])

        plt.title("Assignment 3 (RBE 550): Valet"), plt.xlim((0,self.world.size[0])), plt.ylim((0,self.world.size[1]))
        plt.show()
        return path_x, path_y, path_theta

    def collision_check(self, state) -> bool:
        
        for index in range(len(self.obstacles_x)):
            x_left = self.obstacles_x[index][0]  # indexing a tuple 
            x_right = self.obstacles_x[index][1]
            y_left = self.obstacles_y[index][0]
            y_right = self.obstacles_y[index][1]

            if (round(state.x) in range(x_left, x_right+1)) and (round(state.y) in range(y_left, y_right + 1)):
                self.add_to_closed(state)  # state causes collision and is added to closed as a result
                print("Collision Occurred")
                return True
        return False
    
    def plan(self):
        print("Beginning A* Planning")
        print(f"Starting Location: {(self.start.x, self.start.y, self.start.theta)}")
        print(f"Goal Location: {self.goal}")

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
            # print(idx)
            if idx == 5000: 
                path_x, path_y, path_theta = self.show_path(q)
                self.simulate(path_x, path_y, path_theta)
                break
            print(f"x: {q.x}, y: {q.y}, theta: {q.theta}")
            self.open.pop(self.open.index(q))
            self.add_to_closed(q)
            # search for the surrounding neighbors
 
            neighbors = self.get_neighbors(q, timestep = 1)

            previous_f = neighbors[0].f

            for neighbor in neighbors:
                if self.goal_check(neighbor):
                    print("Goal found!")
                    path_x, path_y, path_theta = self.show_path(q)
                    self.simulate(path_x, path_y, path_theta)
                    goal_found = True
                    break
                elif neighbor not in self.closed:
                    neighbor.g = neighbor.calculate_g(neighbor.parent)
                    neighbor.h = neighbor.calculate_h(self.goal)
                    neighbor.f = neighbor.calculate_f()
                    
                    if neighbor.f < previous_f:
                        q = neighbor
                        previous_f = neighbor.f

                # for node in self.open:  # checking the open list
                #     if (q.x, q.y, q.theta) == (node.x, node.y, node.theta) or (node.f < q.f):
                #         continue

                # for node in self.closed:  # checking the closed list
                #     if (q.x, q.y, q.theta) == (node.x, node.y, node.theta) or (node.f < q.f):
                #         continue
                
                self.add_to_open(q)



        print("Goal has been found, timeout has been reached, or open list is empty")
            


    def refine_c_space(self, state: State, obstacle_location): # function to avoid creation of states where obstacles exist
        if (state.x in obstacle_location.x) or (state.y in obstacle_location.y):
            self.add_to_closed(state)
    
    def goal_check(self, state: State):
        # current_state = (state.x, state.y, state.theta) 
        current_state = (round(state.x,1), round(state.y,1))
        # if current_state == self.goal: 
        #     return True
        
        if current_state == (self.goal[0], self.goal[1]): 
            return True

        return False

    def exceeds_world_limits(self, x, y) -> bool: 
        if (x < 0) or (x > self.world.size[0]): 
            # print("Exceeds limits")
            return True
        elif (y < 0) or (y > self.world.size[1]):
            # print("Exceeds limits")
            return True
        else: 
            return False
        
    def get_neighbors(self, state, timestep = 0.1) -> List[State]:
        if isinstance(state, State):
            neighbors = []

            # what are all possible options to go to? I need to vary my position (x,y, theta) with the velocity equations
            # my inputs are for lecture 10, slide 26 is vl and vr. Combinations of each wheel's velocities
            
            R = 1 # wheel radius
            L = 4  # distance between wheels

            max_speed = 5

            speeds = []

            for speed in range(-max_speed, max_speed+1): # looping to get all possible speed combos for the two wheels
                speeds.append((speed, max_speed))
                speeds.append((max_speed, speed))
            
            speeds.sort()
            speeds.pop()
            
            for speed in speeds: 
                # calculating velocity and position with each speed combo
                vr, vl = speed[0], speed[1]
                        
                theta_dot = (R/L)*(vr - vl)
                theta =  state.theta + (theta_dot*timestep)  # should already be in radians

                theta = round(theta % (2*pi),2)

                x_dot = (R/2)*(vr + vl)*cos(theta)
                x = round(state.x + (x_dot * timestep),2)
                

                y_dot = (R/2)*(vr + vl)*sin(theta)
                y = round(state.y + (y_dot * timestep),2)

                # print(f" (x_dot, y_dot, theta_dot): {x_dot, y_dot, theta_dot}")

                if self.exceeds_world_limits(x, y): 
                    continue
                else:
                    neighbor_state = State(x, y, theta, velocity= Point(x_dot, y_dot))
                    neighbor_state.vr = vr
                    neighbor_state.vl = vl
                    neighbor_state.parent = state
                    neighbors.append(neighbor_state)
            
            return neighbors
        else:
            return 0



