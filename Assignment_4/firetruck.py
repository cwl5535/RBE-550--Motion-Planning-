from probabilistic_road_map import prm_planning
from matplotlib import pyplot as plt

class Firetruck(): 
    def __init__(self): 
        self.x = None
        self.y = None

    def plan(self, ox, oy, sx, sy, gx, gy):
        self.x = sx
        self.y = sy

        path_x, path_y = prm_planning(sx, sy, gx, gy, ox, oy, robot_radius = 1)

        alert = f"Cannot find path between {(sx, sy)} and {gx, gy}"
        
        try:
            assert path_x, alert
        except: 
            AssertionError

        return path_x, path_y
    
    def search_for_nearby_open(self, burning_obstacle: tuple, open_nodes:list) -> tuple:
        # need to search for open spot adjacent to burning obstacle
        x = burning_obstacle[0]
        y = burning_obstacle[1]

        radius = 5

        north = (x, y+radius)
        south = (x, y-radius)
        east = (x+radius, y)
        west = (x-radius, y)
        northeast = (x+radius, y+radius)
        southeast = (x+radius, y-radius)
        southwest = (x-radius, y-radius)
        northwest = (x-radius, y+radius)
        # print(type(north))
        directions = [north, south, east, west, northeast, northwest, southeast, southwest]

        for direction in directions:
            
            if direction in open_nodes:
                
                return direction

    
    
    def move(self,path_x, path_y):
        plt.plot(path_x, path_y, "-r")
        plt.pause(0.001)
        # plt.show()




# def main(rng=None):
#     # print(__file__ + " start!!")

#     # start and goal position
#     sx = 10.0  # [m]
#     sy = 10.0  # [m]
#     gx = 50.0  # [m]
#     gy = 50.0  # [m]
#     robot_size = 5.0  # [m]

    # if show_animation:
    #     plt.plot(ox, oy, ".k")
    #     plt.plot(sx, sy, "^r")
    #     plt.plot(gx, gy, "^c")
    #     plt.grid(True)
    #     plt.axis("equal")


# if __name__ == '__main__':
#     main()
