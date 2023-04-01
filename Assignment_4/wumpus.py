from a_star import AStarPlanner
from matplotlib import pyplot as plt


# use A* to move to obstacle locations and set 


class Wumpus(): 
    def __init__(self): 
        self.x = None
        self.y = None
        self.goal_found = False
        # self.planner = AStarPlanner(None, None, 1, 1)

    def plan(self, ox, oy, sx, sy, gx, gy):
        # print(__file__ + " start!!")

        # start and goal position
        # sx = 10.0  # [m]
        # sy = 10.0  # [m]
        # gx = 50.0  # [m]
        # gy = 50.0  # [m]
        self.x = sx
        self.y = sy
        grid_size = 1.0  # [m]
        robot_radius = 1.0  # [m]

        # if show_animation:  # pragma: no cover
        #     plt.plot(ox, oy, ".k")
        #     plt.plot(sx, sy, "og")
        #     plt.plot(gx, gy, "xb")
        #     plt.grid(True)
        #     plt.axis("equal")

        a_star = AStarPlanner(ox, oy, grid_size, robot_radius)
        path_x, path_y = a_star.planning(sx, sy, gx, gy)


        assert path_x, "Cannot find path"
        
        self.goal_found = a_star.goal_found

        return path_x, path_y
    
    def move(self, path_x, path_y):
        plt.plot(path_x, path_y, "-r")
        plt.pause(0.001)
        # plt.show()
    