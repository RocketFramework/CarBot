from .car_config import  MINIMUM_GAP, WHEEL_RADIUS, ONE_WHEEL_TURN_LENGTH, ONE_WHEEL_TURN_STEPS
import math
import time

from .classes.lida_sensor import LidarSensor
from .classes.car_engine import CarEngine

class Auto_Pilot:
    def __int__(self):
        pass
    
    def find_direction(self):
        # Get the input from lida
        self.lidarSensor = LidarSensor()
        self.carEngine = CarEngine()
        distance = self.lidarSensor.get_distance_to_obstacle()
        # if a distance is long enough
        if distance > MINIMUM_GAP:
            steps = int(((distance - MINIMUM_GAP)/ONE_WHEEL_TURN_LENGTH) * ONE_WHEEL_TURN_STEPS)
            # Move the car forward
            self.carEngine.move_forward(steps)
        else:
            #Move head to left
            #TBD
            distance_l = self.lidarSensor.get_distance_to_obstacle()
            #wait   
            time.sleep(1)
            #Move head to right
            #TBD
            distance_r = self.lidarSensor.get_distance_to_obstacle()
            #find the direction that has move space
            if (distance_l > distance_r):
                distance = distance_l
            else:
                distance = distance_r
        # else
        # trun the car and get the input from Lida
    
# Get all the input from
# LIDA
# Camera
# Then Move
# or Turn and Get the input again until it can move