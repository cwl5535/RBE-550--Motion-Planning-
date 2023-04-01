from probabilistic_road_map import prm_planning
from matplotlib import pyplot as plt

class Firetruck(): 
    def __init__(self): 
        self.x = None
        self.y = None

    def plan(self, ox, oy, sx, sy, gx, gy):
        self.x = sx
        self.y = sy

        path_x, path_y = prm_planning(sx, sy, gx, gy, ox, oy, robot_size = 5)

        assert path_x, "Cannot find path"

        return path_x, path_y
    
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
