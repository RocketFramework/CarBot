from Car.Hardware.compass import Gy273
from Car.config import COMPASS_ACCURACY, DRIVER_DEFAULT_ANGLE, DRIVER_MAX_ANGLE, DRIVER_MIN_ANGLE, MAX_DIFF_TIME
import time
from LOG.Logger import Logger
from collections import deque
from enum import Enum

class Directions(Enum):
    North = 0
    East = 90
    South = 180
    West = 270

class Car_Navigator:
    def __init__(self):
        self.compass = Gy273()
        self.current_heading = self.compass.get_heading_angle()
        self.target_heading = 0
        self.accuracy = COMPASS_ACCURACY
        self.current_time = time.monotonic()
        self.time_array = deque(maxlen=6)
        self.stuck = bool()
        self.Logger = Logger()

    def set_target_heading(self, angle: int):
        self.target_heading = angle

    def calc_diff_to_target(self, target: int) -> int:
        self.current_heading = self.compass.get_heading_angle()
        diff = target - self.current_heading
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        return diff

    def smart_dir_calc(self, target: int) -> int:
        dir = self.compass.get_heading_angle()
        if target > DRIVER_DEFAULT_ANGLE:
            target = dir + target
        elif target < DRIVER_DEFAULT_ANGLE:
            target = dir - target
        diff = self.calc_diff_to_target(target)
        if abs(diff) <= self.accuracy:
            return DRIVER_DEFAULT_ANGLE
        if diff <= -50:
            return DRIVER_MIN_ANGLE   
        elif diff >= 50:
            return DRIVER_MAX_ANGLE   

        return 25 + int((diff / 50) * 25)

    def stuck_detection_logic(self):
        current_time = time.time()
        self.time_array.append(current_time)
        if len(self.time_array) == 6:
            A = self.time_array[5] - self.time_array[4]
            B = self.time_array[4] - self.time_array[3]
            C = self.time_array[3] - self.time_array[2]
            D = self.time_array[2] - self.time_array[1]
            E = self.time_array[1] - self.time_array[0]
            self.Logger.log(
                                "info", f"Time Array:\n A:{A}\n B:{B}\n C:{C}\n D:{D}\n E:{E}")           
            if (abs(A - B) <= MAX_DIFF_TIME 
                and abs(B - C) <= MAX_DIFF_TIME 
                and abs(C - D) <= MAX_DIFF_TIME 
                and abs(D - E) <= MAX_DIFF_TIME):
                
                self.stuck = True
                self.Logger.log(
                                "info", "The car is assumed to be stuck in the same position.")
            elif (abs(A - C) <= MAX_DIFF_TIME
                  and abs(C - E) <= MAX_DIFF_TIME 
                  and abs(B - D) <= MAX_DIFF_TIME):
                self.stuck = True
                self.Logger.log(
                                "info", "The car is assumed to be stuck in the same position.")
            else:
                self.stuck = False
            
        return self.stuck