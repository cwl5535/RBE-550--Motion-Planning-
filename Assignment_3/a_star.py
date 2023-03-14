from math import sqrt, pi, inf, radians, cos, sin
from typing import List
from matplotlib import pyplot as plt
import numpy as np
import time
from geometry import Point
from world import World
from agents import Car, RectangleBuilding
from create_world import create_world


# dt = 0.1
# w = World(dt, width = 120, height = 120, ppm = 6)

# w.add(RectangleBuilding(Point(60,1), Point(120,2), 'gray26'))  # bottom border
# w.add(RectangleBuilding(Point(60,119), Point(120,2), 'gray26')) # top border
# w.add(RectangleBuilding(Point(1,60), Point(2,120), 'gray26'))  # left border
# w.add(RectangleBuilding(Point(119,60), Point(2,120), 'gray26'))  # right border

# # A Car object is a dynamic object -- it can move. We construct it using its center location and heading angle.
# car = Car(Point(15, 110), 0, color = "green")

# # parked_car1 = Car(Point(15, 10), 0)
# parked_car1 = RectangleBuilding(Point(25, 10), Point(20,10), 'red')
# # parked_car2 = Car(Point(90,10), 0)
# parked_car2 = RectangleBuilding(Point(80,10), Point(20,10), 'red')
# obstacle = RectangleBuilding(Point(70,70), Point(40,25), 'black')

# w.add(car)
# w.add(parked_car1)
# w.add(parked_car2)
# w.add(obstacle)



class State():
    def __init__(self, x = 0, y = 0, theta = 0, velocity = Point(0,0), past_cost = inf): 

        #self.cost_to_go = self.distance_to_goal(goal) # going to be calculated with Euclidean formulas 
        self.g = past_cost
        self.h = 0
        self.f = 0
        self.x = x
        self.y = y
        self.theta = theta # possible states are 0 to 2pi, in 15 degree intervals
        self.parent = None
        self.velocity = velocity

    def distance_to(self, to) -> float:
        if isinstance(to, tuple):
            delta_x = (self.x - to[0])
            delta_y = (self.x - to[1])
        else:
            delta_x = (self.x - to.x)
            delta_y = (self.y - to.y)
        dist = round(sqrt((delta_x**2) + (delta_y**2)),2)
        return dist
    
    def calculate_g(self, next_state) -> float:
        # Distance Cost 

        dist_cost = self.g + self.distance_to(next_state)

        # Steering Cost

        steering_cost = abs(self.theta - next_state.theta)

        total_cost = round(dist_cost + steering_cost,2)

        return total_cost

    def calculate_h(self, goal):
        return self.distance_to(goal)
    
    def calculate_f(self):
        return self.g + self.h
    

class AStar():
    def __init__(self, car, start: tuple, goal: tuple):

        self.start = State(start[0], start[1], start[2], past_cost = 0)  # start should be a 3 element tuple, with x y and theta values
        self.goal = goal
        self.open = [self.start]
        self.closed = []
        self.path = [State(start, past_cost = 0)]
        self.car = car
        
    def add_to_open(self, state):
        self.open.append(state)

    def add_to_closed(self, state):
        self.closed.append(state)

    def simulate(self, current_state, car, world):
        self.car.velocity = current_state.velocity
        self.car.inputSteering = current_state.theta
        world.tick()
        world.render()
        time.sleep(dt/4)
    
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
    def plan(self):

        # self.add_to_open(self.start)
        

        while len(self.open) > 0:
            print(f"Open list has {len(self.open)} states")
            current = self.open[0]
            self.simulate(current)
            self.open.pop(self.open.index(current))
            self.add_to_closed(current)

            if self.goal_check(current):
                print("Goal found")
                self.show_path(current)
                break

            # search for the surrounding neighbors
 
            neighbors = self.get_neighbors(current)

            for neighbor in neighbors: 
                if neighbor not in self.closed:
                    
                    

                    tentative_g = current.calculate_g(neighbor)

                    if tentative_g < neighbor.g:
                        neighbor.g = tentative_g
                        neighbor.parent = current
                        neighbor.h = neighbor.calculate_h(self.goal)
                        neighbor.f = neighbor.calculate_f()
                        self.add_to_open(neighbor)
            


    def refine_c_space(self, state: State, obstacle_location): # function to avoid creation of states where obstacles exist
        if (state.x in obstacle_location.x) or (state.y in obstacle_location.y):
            self.add_to_closed(state)
    
    def goal_check(self, state: State):
        current_state = (state.x, state.y, state.theta) 

        if current_state == self.goal: 
            return True
        
        return False

    def get_neighbors(self, state, timestep = 0.1):
        if isinstance(state, State):
            neighbors = []

            # what are all possible options to go to? I need to vary my position (x,y, theta) with the velocity equations
            # my inputs are for lecture 10, slide 26 is vl and vr. Combinations of each wheel's velocities
            
            R = 1
            L = 2
            max_speed = 10

            speeds = []

            for speed in range(1, max_speed+1): # looping to get all possible speed combos for the two wheels
                speeds.append((speed, max_speed))
                speeds.append((max_speed, speed))
            
            speeds.sort()
            
            for speed in speeds: 
                # calculating velocity and position with each speed combo
                vr, vl = speed[0], speed[1]
                            
                theta_dot = (R/L)*(vr + vl)
                theta =  state.theta + (theta_dot*timestep) 

                x_dot = (R/2)*(vr + vl)*cos(theta)
                x = state.x + (x_dot * timestep)
                

                y_dot = (R/2)*(vr + vl)*sin(theta)
                y = state.y + (y_dot * timestep)

                neighbor_state = State(x, y, theta, velocity= Point(x_dot, y_dot))
                neighbors.append(neighbor_state)
            
            return neighbors
        else:
            return 0

if __name__ == "__main__":
    planner = AStar((0,0,0), (30, 35, 0))
    planner.plan()
        


