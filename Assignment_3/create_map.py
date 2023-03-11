import numpy as np
import time
from geometry import Point
from world import World
from agents import Car, RectangleBuilding


dt = 0.1
w = World(dt, width = 120, height = 120, ppm = 6)

w.add(RectangleBuilding(Point(60,1), Point(120,2), 'gray26'))  # bottom border
w.add(RectangleBuilding(Point(60,119), Point(120,2), 'gray26')) # top border
w.add(RectangleBuilding(Point(1,60), Point(2,120), 'gray26'))  # left border
w.add(RectangleBuilding(Point(119,60), Point(2,120), 'gray26'))  # right border

# A Car object is a dynamic object -- it can move. We construct it using its center location and heading angle.
car = Car(Point(15, 110), 0, color = "green")

# parked_car1 = Car(Point(15, 10), 0)
parked_car1 = RectangleBuilding(Point(25, 10), Point(20,10), 'red')
# parked_car2 = Car(Point(90,10), 0)
parked_car2 = RectangleBuilding(Point(80,10), Point(20,10), 'red')
obstacle = RectangleBuilding(Point(70,70), Point(40,25), 'black')

w.add(car)
w.add(parked_car1)
w.add(parked_car2)
w.add(obstacle)


inc = 0
for k in range(500): 
    # inc += 1
    # car.set_control(-0.5,0.25)
    w.tick()
    w.render()
    time.sleep(dt/4)
w.close()
