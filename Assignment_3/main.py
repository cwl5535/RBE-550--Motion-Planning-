from create_world import create_world
from a_star import AStar, State
from agents import Car
from geometry import Point
from numpy import pi

if __name__ == "__main__":

    vehicle = "skid"
    start = (20, 100, -pi/2)  # heading angle must be in radians
    parking_spot = (55,15,0)


    # parking_spot = (25,100, 0)
    # parking_spot = (90,60,0) # collision test, this is where one of the obstacles is    

    world_size = 120
    world, obstacle_x_ranges, obstacle_y_ranges = create_world(vehicle, world_size)


    car = Car(Point(start[0], start[1]), start[2], vehicle_type= vehicle)
    world.add(car)




    planner = AStar(car = car,
                    obstacles_x =  obstacle_x_ranges, 
                    obstacles_y = obstacle_y_ranges, 
                    world = world,
                    start = start,
                    goal= parking_spot
                    )
    planner.plan()