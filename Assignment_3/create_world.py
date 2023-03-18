import numpy as np
import time
from geometry import Point
from world import World
from agents import RectangleBuilding, Car
from typing import List, Tuple

def create_world(world_type: str, world_size=120) -> Tuple[World, List[Tuple], List[Tuple]] :
    if world_type == "skid":

        dt = 0.1
        w = World(dt, width = world_size, height = world_size, ppm = 6)

        # Adding Borders
        bottom = RectangleBuilding(Point(world_size//2,1), Point(world_size,2), 'gray26')  # bottom border
        top = RectangleBuilding(Point(world_size//2,119), Point(world_size,2), 'gray26') # top border
        left = RectangleBuilding(Point(1,world_size//2), Point(2,world_size), 'gray26')  # left border
        right = RectangleBuilding(Point(world_size - 1,world_size//2), Point(2,world_size), 'gray26')  # right border

        w.add(bottom)
        w.add(top)
        w.add(left)
        w.add(right)

        # A Car object is a dynamic object -- it can move. We construct it using its center location and heading angle.
        # car = Car(Point(15, 110), 0, color = "green")

        parked_car1 = RectangleBuilding(Point(25, 10), Point(20,10), 'red')
        parked_car2 = RectangleBuilding(Point(80,10), Point(20,10), 'red')
        obstacle = RectangleBuilding(Point(90,70), Point(40,25), 'black')

        # w.add(car)
        w.add(parked_car1)
        w.add(parked_car2)
        w.add(obstacle)

        obstacle_x_regions = [bottom.x_range, top.x_range, left.x_range, right.x_range, parked_car1.x_range, parked_car2.x_range, obstacle.x_range]
        obstacle_y_regions = [bottom.y_range, top.y_range, left.y_range, right.y_range,parked_car1.y_range, parked_car2.y_range, obstacle.y_range]    

    return w, obstacle_x_regions, obstacle_y_regions
