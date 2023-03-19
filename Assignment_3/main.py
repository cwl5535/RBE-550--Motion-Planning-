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

planner = AStar(car,
                obstacle_x_ranges, obstacle_y_ranges, 
                world,
                (car_center[0], car_center[1],car_angle),
                (car_center[0]+25, car_center[1]-50,car_angle - round(pi/2,2))
                )
planner.plan()