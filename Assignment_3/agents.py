from entities import RectangleEntity, CircleEntity, RingEntity
from geometry import Point

# For colors, we use tkinter colors. See http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

class Car(RectangleEntity):
    def __init__(self, center: Point, heading: float, vehicle_type: str):
        size = Point(20., 10.)  # changed from (4., 2.) on 3-6-23
        movable = True
        friction = 0.06
        super(Car, self).__init__(center, heading, size, movable, friction)
        # self.color = color
        self.collidable = True
        self.vehicle_type = vehicle_type
        if vehicle_type == "skid": 
            self.color = "green"
        elif vehicle_type == "car":
            self.color == "blue"
        elif vehicle_type == "truck": 
            self.color == "gray"
            
        
class Pedestrian(CircleEntity):
    def __init__(self, center: Point, heading: float, color: str = 'LightSalmon3'): # after careful consideration, I decided my color is the same as a salmon, so here we go.
        radius = 0.5
        movable = True
        friction = 0.2
        super(Pedestrian, self).__init__(center, heading, radius, movable, friction)
        self.color = color
        self.collidable = True
        
class RectangleBuilding(RectangleEntity):
    def __init__(self, center: Point, size: Point, color: str = 'gray26'):
        heading = 0.
        movable = False
        friction = 0.
        super(RectangleBuilding, self).__init__(center, heading, size, movable, friction)
        self.color = color
        self.collidable = True
        self.x_range = (int(center.x) - (int(size.x)//2), int(center.x) + (int(size.x)//2))
        self.y_range = (int(center.y) - (int(size.y)//2), int(center.y) + (int(size.y)//2))
        
class CircleBuilding(CircleEntity):
    def __init__(self, center: Point, radius: float, color: str = 'gray26'):
        heading = 0.
        movable = False
        friction = 0.
        super(CircleBuilding, self).__init__(center, heading, radius, movable, friction)
        self.color = color
        self.collidable = True

class RingBuilding(RingEntity):
    def __init__(self, center: Point, inner_radius: float, outer_radius: float, color: str = 'gray26'):
        heading = 0.
        movable = False
        friction = 0.
        super(RingBuilding, self).__init__(center, heading, inner_radius, outer_radius, movable, friction)
        self.color = color
        self.collidable = True

class Painting(RectangleEntity):
    def __init__(self, center: Point, size: Point, color: str = 'gray26', heading: float = 0.):
        movable = False
        friction = 0.
        super(Painting, self).__init__(center, heading, size, movable, friction)
        self.color = color
        self.collidable = False
