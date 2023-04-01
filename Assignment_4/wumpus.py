from a_star import AStarPlanner
from matplotlib import pyplot as plt


# use A* to move to obstacle locations and set 


class Wumpus(): 
    def __init__(self): 
        self.x = None
        self.y = None
        # self.goal_found = False
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
        
        # self.goal_found = a_star.goal_found

        return path_x, path_y
    
    def move(self, path_x, path_y):
        plt.plot(path_x, path_y, "-r")
        plt.pause(0.001)
        plt.show()

if __name__ == "__main__":
    # wumpus = Wumpus()

    # ox, oy = [], []
    # for i in range(0, 250):
    #     ox.append(i)
    #     oy.append(0)
    # for i in range(0, 250):
    #     ox.append(0)
    #     oy.append(i)
    # for i in range(0, 250):
    #     ox.append(i)
    #     oy.append(250)
    # for i in range(0, 250):
    #     ox.append(250)
    #     oy.append(i)

    # path_x, path_y = wumpus.plan(ox,oy, 1,1, 50, 50)
    # wumpus.move(path_x=path_x, path_y=path_y)

    from pure_pursuit import State, States, TargetCourse, proportional_control, pure_pursuit_steer_control, plot_arrow 
    import numpy as np
        #  target course
        
    # cx = np.arange(1,50)
    # cy = np.arange(1,50)
    cx_u = [50.0, 49.0, 48.0, 47.0, 46.0, 45.0, 44.0, 43.0, 42.0, 41.0, 40.0, 39.0, 38.0, 37.0]
    cx = cx_u.sort()
    cy_u = [50.0, 49.0, 48.0, 47.0, 46.0, 45.0, 44.0, 43.0, 42.0, 41.0, 40.0, 39.0, 38.0, 37.0]
    cy = cy_u.sort()
    show_animation = True 

    target_speed = 10.0 / 3.6  # [m/s]

    T = 100.0  # max simulation time

    # initial state
    state = State(x=1, y=1, yaw=0.0, v=0.0)

    lastIndex = len(cx) - 1
    time = 0.0
    states = States()
    states.append(time, state)
    target_course = TargetCourse(cx, cy)
    target_ind, _ = target_course.search_target_index(state)

    while T >= time and lastIndex > target_ind:

        # Calc control input
        ai = proportional_control(target_speed, state.v)
        di, target_ind = pure_pursuit_steer_control(
            state, target_course, target_ind)

        state.update(ai, di)  # Control vehicle

        time += 0.1
        states.append(time, state)

        if show_animation:  # pragma: no cover
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
            plot_arrow(state.x, state.y, state.yaw)
            plt.plot(cx, cy, "-r", label="course")
            plt.plot(states.x, states.y, "-b", label="trajectory")
            plt.plot(cx[target_ind], cy[target_ind], "xg", label="target")
            plt.axis("equal")
            plt.grid(True)
            plt.title("Speed[km/h]:" + str(state.v * 3.6)[:4])
            plt.pause(0.001)

    # Test
    assert lastIndex >= target_ind, "Cannot goal"

    if show_animation:  # pragma: no cover
        plt.cla()
        plt.plot(cx, cy, ".r", label="course")
        plt.plot(states.x, states.y, "-b", label="trajectory")
        plt.legend()
        plt.xlabel("x[m]")
        plt.ylabel("y[m]")
        plt.axis("equal")
        plt.grid(True)

        plt.subplots(1)
        plt.plot(states.t, [iv * 3.6 for iv in states.v], "-r")
        plt.xlabel("Time[s]")
        plt.ylabel("Speed[km/h]")
        plt.grid(True)
        plt.show()
