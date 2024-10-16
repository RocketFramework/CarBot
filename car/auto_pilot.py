from .car_config import  MINIMUM_GAP, WHEEL_RADIUS, ONE_WHEEL_TURN_LENGTH, ONE_WHEEL_TURN_STEPS
import math
import time
from typing import List
from .classes.lida_sensor import LidarSensor
from .classes.car_engine import CarEngine
from .classes.car_driver import CarFront
from .classes.car_eye import CarEye
from .classes.class_config import GPIO 

class Auto_Pilot:
    def __int__(self):
        GPIO.setmode(GPIO.BOARD)
    
    def run(self):
    # Get the input from lidar
        self.lidarSensor = LidarSensor()
        self.carEngine = CarEngine()
        self.carDriver = CarFront()
        self.carEye = CarEye()
        
        # Obtain distance from the LIDAR
        distance = self.lidarSensor.get_distance_to_obstacle()
        print(f"Distance To Obstacle in front: {distance} m")
        input_datas = [(0,0)]  # Initialize as an empty list

        # If a distance is long enough
        if distance > MINIMUM_GAP:
            steps = int(((distance - MINIMUM_GAP) / ONE_WHEEL_TURN_LENGTH) * ONE_WHEEL_TURN_STEPS)
            # Move the car forward
            self.carEngine.move_forward(steps)
        else:
            # Move head to left
            out_datas = [True, 0.0]
            while out_datas[0]:
                out_datas = self.carEye.turn_left()
                distance_l = self.lidarSensor.get_distance_to_obstacle()
                print(f"Distance To Obstacle in left: {distance} m")
                # Wait   
                time.sleep(1)
                input_datas.append((out_datas[1], distance_l))  # Consistent tuple use

            out_datas[0] = True  
            self.carEye.set_angle(70) 
            # Move head to right
            while out_datas[0]:
                out_datas = self.carEye.turn_right()
                distance_r = self.lidarSensor.get_distance_to_obstacle()
                print(f"Distance To Obstacle in right: {distance} m")
                # Wait   
                time.sleep(1)
                # When distance is higher we need the angle as well at the time
                input_datas.append((out_datas[1], distance_r))  # Consistent tuple use

        # Ensure input_datas is not empty to avoid ValueError
        if input_datas:
            max_item = max(input_datas, key=lambda x: x[1])
            moving_angle, to_move_distance = max_item
            self.carDriver.set_front_angle(moving_angle)
            self.carEngine.move_forward(int(((to_move_distance - MINIMUM_GAP) / ONE_WHEEL_TURN_LENGTH) * ONE_WHEEL_TURN_STEPS))
          # we need the distance and the angle of the eye motor
            # then we need a mapping of what angle of the eye motor means to the driver motor
            # then we need to turn the eye motor to its default location and also 
            # turn the driver motor to the desired calculated position
            # then we need to make the car move
            # we need to keep repeating this forever
            #find the direction that has move space

        # else
        # trun the car and get the input from Lida
    
# Get all the input from
# LIDA
# Camera
# Then Move
# or Turn and Get the input again until it can move
