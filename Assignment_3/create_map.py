import numpy as np
import time
from geometry import Point
from world import World
from agents import Car, RectangleBuilding


dt = 0.1
w = World(dt, width = 120, height = 120, ppm = 6)

w.add(RectangleBuilding(Point(60,1), Point(120,2), 'gray26'))
w.add(RectangleBuilding(Point(60,119), Point(120,2), 'gray26'))
w.add(RectangleBuilding(Point(1,60), Point(2,120), 'gray26'))
w.add(RectangleBuilding(Point(119,60), Point(2,120), 'gray26'))

for k in range(500): 
    w.tick()
    w.render()
    time.sleep(dt/4)
w.close()
