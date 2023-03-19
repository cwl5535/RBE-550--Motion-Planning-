from create_world import create_world
from a_star import AStar, State
from agents import Car
from geometry import Point
from numpy import pi

world_size = 120
world, obstacle_x_ranges, obstacle_y_ranges = create_world("skid", world_size)

car_center = (20,80)
car_angle = 0 # This is in radians
car = Car(Point(car_center[0], car_center[1]), car_angle, color = "green")
world.add(car)

# sim test
# for i in range(500): 
#     world.tick()
#     world.render()
#     time.sleep(0.1/4)
# world.close()

# TODO need to figure out why angles are everywhere, how the steering in CARLO works
# TODO Wheels aren't given the ability to drive in reverse, only positive values

planner = AStar(car,
                obstacle_x_ranges, obstacle_y_ranges, 
                world,
                (car_center[0], car_center[1],car_angle),
                (car_center[0]+25, car_center[1]-50,car_angle - round(pi/2,2))
                )
planner.plan()