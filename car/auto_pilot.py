from .car_config import  MINIMUM_GAP, WHEEL_RADIUS, ONE_WHEEL_TURN_LENGTH, ONE_WHEEL_TURN_STEPS
import math
import time

from .classes.lida_sensor import LidarSensor
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.car_eye import CarEye

class Auto_Pilot:
    def __int__(self):
        pass
    
    def find_direction(self):
        # Get the input from lida
        self.lidarSensor = LidarSensor()
        self.carEngine = CarEngine()
        self.carDriver = CarDriver()
        self.carEye = CarEye()
        distance = self.lidarSensor.get_distance_to_obstacle()
        # if a distance is long enough
        if distance > MINIMUM_GAP:
            steps = int(((distance - MINIMUM_GAP)/ONE_WHEEL_TURN_LENGTH) * ONE_WHEEL_TURN_STEPS)
            # Move the car forward
            self.carEngine.move_forward(steps)
        else:
            #Move head to left
            while self.carEye.turn_left():
                distance_l = self.lidarSensor.get_distance_to_obstacle()
                #wait   
                time.sleep(1)
                #When distance is heigher we need the angle as well at the time
                distance = max(distance_l, distance)
            #Move head to right
            while self.carEye.turn_right():
                distance_r = self.lidarSensor.get_distance_to_obstacle()
                #wait   
                time.sleep(1)
                #When distance is heigher we need the angle as well at the time
                distance = max(distance_r, distance)
            # we need the distance and the angle of the eye motor
            # then we need a mapping of what angle of the eye motor means to the driver motor
            # then we need to turn the eye motor to its default location and also 
            # turn the driver motor to the desired calculated position
            # then we need to make the car move
            # we need to keep repeating this forever
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