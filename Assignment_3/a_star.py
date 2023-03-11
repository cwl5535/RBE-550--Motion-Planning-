import math

class AStar():
    def __init__(self): 
        self.open = []
        self.past = 0
    


class State():
    def __init__(self, x, y, theta): 
        self.cost_to_go = 0  # going to be calculated with Euclidean formulas 
        self.x = x
        self.y = y
        self.theta = theta # possible states are 0 to 2pi
    def distance_to_goal(self, goal)
        dist = math.sqrt(self.x**2 + self.y**2)

