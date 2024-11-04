import time
import random
from car.car_config import MINIMUM_GAP
class UltrasonicSensor:
    def __init__(self):
        self.distance = int()
        
    def get_distance_to_obstacle(self):
        self.ditance = round(random.uniform(1.5, 5.5), 2)
        return self.distance
    
    def can_keep_moving(self):
        time.sleep(0.001)
        self.ditance = round(random.uniform(1.5, 5.5), 2)
        if self.distance > MINIMUM_GAP:
            return True
        else:
            return False
        