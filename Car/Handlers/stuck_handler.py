from Car.config import MINIMUM_SPEED, MINIMUM_DISTANCE_BACK, MID_GAP, DRIVER_MAX_ANGLE, DRIVER_MIN_ANGLE, EYE_MIN_ANGLE, EYE_MAX_ANGLE
from LOG.Logger import Logger
import time

class StuckHandler:
    def __init__(self, car, running_ref):
        self.Car = car
        self.Logger = Logger()
        self.handling_stuck = False
        self.running_ref = running_ref
        self.last_max_angle = None
        
    def method_1(self):
        self.Logger.log("info", "Stuck Handler: Method 1 initiated.")
        self.Car.CarEngine.move_reverse(50)
        start_time = time.monotonic()
        distance_back = self.Car.CarSensor.rear_ultrasonic.get_distance()
        while time.monotonic() - start_time < 10 and distance_back > MINIMUM_DISTANCE_BACK:
            distance_back = self.Car.CarSensor.rear_ultrasonic.get_distance()
            if not self.running_ref():
                self.Car.CarEngine.stop()
                return

        self.Car.CarEngine.stop()
        if self.last_max_angle != DRIVER_MAX_ANGLE:
            turning_angle = DRIVER_MAX_ANGLE
        else:
            turning_angle = DRIVER_MIN_ANGLE
            
        self.Car.CarDriver.set_angle(turning_angle, 1)
        self.last_max_angle = turning_angle
        
        if turning_angle == DRIVER_MAX_ANGLE:
            self.Car.CarEye.set_angle(EYE_MIN_ANGLE)
        else:
            self.Car.CarEye.set_angle(EYE_MAX_ANGLE)
            
        self.Car.CarEngine.move_forward(MINIMUM_SPEED)
        
    def method_2(self):
        self.Logger.log("info", "Stuck Handler: Method 2 initiated.")
        self.handling_stuck = True
        self.rear_dist = self.Car.CarSensor.rear_ultrasonic.get_distance()
        while self.rear_dist < MINIMUM_DISTANCE_BACK:
            self.rear_dist = self.Car.CarSensor.rear_ultrasonic.get_distance()
            min_dist_front = self.Car.CarSensor.get_min_distance()
            if min_dist_front > MID_GAP:
                return True
            self.Car.move_reverse(MINIMUM_SPEED)
        return False

    def method_3(self):
        self.Logger.log("info", "Stuck Handler: Method 3 initiated.")
        self.handling_stuck = True