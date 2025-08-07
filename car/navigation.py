from .classes.gy273 import Gy273
from enum import Enum

class Directions(Enum):
    N = 0
    NE = 45
    E = 90
    SE = 135
    S = 180
    SW = 225
    W = 270
    NW = 315

class NavigationSystem:
    def __init__(self):
        self.compass = Gy273()
        self.last_turned_direction = None
        self.current_angle = self.compass.get_heading_angle()
        self.current_data = [self.compass.get_heading_direction(angle = self.current_angle), 
                                  self.current_angle]
        
    def get_direction(self):
        return self.compass.get_heading_angle()
    
    def smart_turn(self, target:int):
        current_direction = self.get_direction()
        if current_direction == target:
            turn_data = (0,0)
        else:
            if target - current_direction > 180:
                turn_data = (abs(current_direction - target, 2))  # Turn left
            elif target - current_direction < -180:
                turn_data = (abs(current_direction - target, 1))
            else:
                if self.last_turned_direction is None or self.last_turned_direction == 1:
                    turn_data = (abs(current_direction - target, 2))
                else:
                    turn_data = (abs(current_direction - target, 1))
                self.last_turned_direction = turn_data[1]
        return turn_data
    