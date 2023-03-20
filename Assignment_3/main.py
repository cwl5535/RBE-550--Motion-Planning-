from create_world import create_world
from a_star import AStar, State
from agents import Car
from geometry import Point
from numpy import pi

if __name__ == "__main__":

    world_size = 120
    world, obstacle_x_ranges, obstacle_y_ranges = create_world("skid", world_size)

    car_center = (20,100)
    car_angle = -pi/2 # This is in radians
    car = Car(Point(car_center[0], car_center[1]), car_angle, color = "green")
    world.add(car)

    parking_spot = (55,15,0)
    # parking_spot = (90,60,0) # collision test, this is where one of the obstacles is


    planner = AStar(car = car,
                    obstacles_x =  obstacle_x_ranges, 
                    obstacles_y = obstacle_y_ranges, 
                    world = world,
                    start = (car_center[0], car_center[1],car_angle),
                    goal= parking_spot
                    )
    planner.plan()