from math import sqrt, pi, inf, radians, cos, sin
from typing import List

class State():
    def __init__(self, x = 0, y = 0, theta = 0): 

        #self.cost_to_go = self.distance_to_goal(goal) # going to be calculated with Euclidean formulas 
        self.past_cost = inf()
        self.x = x
        self.y = y
        self.theta = theta # possible states are 0 to 2pi, in 15 degree intervals

    def distance_to_goal(self, goal) -> float:
        delta_x = (self.x - goal.x)
        delta_y = (self.y - goal.y)
        dist = round(sqrt((delta_x**2) + (delta_y**2)),2)
        return dist
    
    def update_cost(self):
        pass
    def set_cost(self, cost):
        self.tentative_cost = cost

class AStar():
    def __init__(self, world_size):

        self.states = self.create_states(world_size)
        self.open = []
        self.closed = []
        # self.past_cost = 0

    def add_to_open(self, state):
        self.open.append(state)

    def add_to_closed(self, state):
        self.closed.append(state)

    def plan(self, goal):
        self.add_to_open(self.states[0])
        while len(self.open) > 0:
            current = self.open[0]
            self.add_to_closed(current)
            self.states.pop(current)

            if self.goal_check(current, goal):
                break
            

            

    def refine_c_space(self, state: State, obstacle_location): # function to avoid creation of states where obstacles exist
        if (state.x in obstacle_location.x) or (state.y in obstacle_location.y):
            self.add_to_closed(state)
    
    def goal_check(state: State, goal: tuple):
        current_state = (state.x, state.y, state.theta) 

        if current_state == goal: 
            return True
        
        return False

    def get_neighbors(state: State, timestep):
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

            neighbor_state = State(x, y, theta)
            neighbors.append(neighbor_state)
        
        return neighbors


        


