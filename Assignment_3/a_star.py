class AStar():
    def __init__(self): 
        self.open = []
        self.past = 0


class State():
    def __init__(self, x, y): 
        self.cost_to_go = 0  # going to be calculated with Euclidean formulas 
        self.x = x
        self.y = y
        