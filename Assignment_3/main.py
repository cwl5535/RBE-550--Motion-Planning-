from create_world import create_world
from a_star import AStar, State
import time
from agents import Car
from geometry import Point

world_size = 120
world, obstacle_x_ranges, obstacle_y_ranges = create_world("skid", world_size)

car = Car(Point(15, 110), 0, color = "green")
world.add(car)

# sim test
# for i in range(500): 
#     world.tick()
#     world.render()
#     time.sleep(0.1/4)
# world.close()

# TODO need to figure out why angles are everywhere, how the steering in CARLO works
# TODO Wheels aren't given the ability to drive in reverse, only positive values
planner = AStar(car, obstacle_x_ranges, obstacle_y_ranges, world, (30,90,0), (30,60,0))
planner.plan()