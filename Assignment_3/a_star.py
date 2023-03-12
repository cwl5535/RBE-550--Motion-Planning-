from math import sqrt, pi, inf, radians, cos, sin
from typing import List

class State():
    def __init__(self, x = 0, y = 0, theta = 0, past_cost = inf()): 

        #self.cost_to_go = self.distance_to_goal(goal) # going to be calculated with Euclidean formulas 
        self.past_cost = past_cost
        self.x = x
        self.y = y
        self.theta = theta # possible states are 0 to 2pi, in 15 degree intervals
        self.parent = None

    def distance_to(self, to) -> float:
        delta_x = (self.x - to.x)
        delta_y = (self.y - to.y)
        dist = round(sqrt((delta_x**2) + (delta_y**2)),2)
        return dist
    
    def calculate_cost(self, goal) -> float:
        # Distance Cost 

        dist_cost = self.distance_to(goal)

        # Steering Cost

        steering_cost = abs(self.theta - goal.theta)

        total_cost = round(dist_cost + steering_cost,2)

        return total_cost

    def set_cost(self, cost):
        self.tentative_cost = cost

class AStar():
    def __init__(self, world_size, start: tuple, goal):

        self.start = State(start, past_cost = 0)  # start should be a 3 element tuple, with x y and theta values
        self.goal = goal
        self.open = []
        self.closed = []
        self.path = [State(start, past_cost = 0)]
        
    def add_to_open(self, state):
        self.open.append(state)

    def add_to_closed(self, state):
        self.closed.append(state)

    def plan(self):

        self.add_to_open(self.start)
        current = self.open[0]

        while len(self.open) > 0:

            self.open.pop()
            self.add_to_closed(current)

            if self.goal_check(current, self.goal):
                break

            # search for the surrounding neighbors
            neighbors = self.get_neighbors(current, timestep=0.1)

            for neighbor in neighbors: 
                neighbor.g_tentative = current.g + neighbor.distance
                neighbor.parent = current

                if neighbor not in self.closed:
                    tentative_cost = neighbor.calculate_cost(goal)
                    neighbor.set_cost(tentative_cost)

                    if neighbor.tentative_cost < neighbor.past_cost:
                    
                        self.open.append(neighbor)
                        


            

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


        


