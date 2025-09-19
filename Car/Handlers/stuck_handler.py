from Car.config import MINIMUM_SPEED, MINIMUM_DISTANCE_BACK, MID_GAP
from LOG.Logger import Logger
import time

class StuckHandler:
    def __init__(self, car):
        self.Car = car
        self.Logger = Logger()
        self.handling_stuck = False
     
    def method_1(self):
        self.Logger.log("info", "Stuck Handler: Method 1 initiated.")
        self.handling_stuck = True
        self.rear_dist = self.Car.CarSensor.rear_ultrasonic.get_distance()
        while self.rear_dist < MINIMUM_DISTANCE_BACK:
            self.rear_dist = self.Car.CarSensor.rear_ultrasonic.get_distance()
            min_dist_front = self.Car.CarSensor.get_min_distance()
            if min_dist_front > MID_GAP:
                return True
            self.car.move_reverse(MINIMUM_SPEED)
        return False
    
    def method_2(self):
        self.Logger.log("info", "Stuck Handler: Method 2 initiated.")
        self.handling_stuck = True
        self.rear_dist = self.Car.CarSensor.rear_ultrasonic.get_distance()

    def method_3(self):
        self.Logger.log("info", "Stuck Handler: Method 3 initiated.")
        self.handling_stuck = True