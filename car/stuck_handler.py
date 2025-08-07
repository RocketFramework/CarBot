import time
from collections import deque
from car.car_config import MID_GAP, MINIMUM_GAP, REAR_MINIMUM_GAP, MAX_DIFF_TIME, MINIMUM_SPEED
from car.memory import Memory
from .classes.car_driver import CarDriver
from .classes.car_engine import CarEngine
from .classes.car_eye import CarEye
from .classes.pca_board import PCABoard
from .classes.class_config import (EYE_MAX_ANGLE, EYE_MIN_ANGLE, DRIVER_DEFAULT_ANGLE,
                                   DRIVER_MAX_ANGLE, DRIVER_MIN_ANGLE)
from .classes.mcp23017 import MCP23017

class StuckHandler:
    """This method can handle when the car is stuck in repetition,
    such as moving orward and backward repeatedly"""
    def __init__(self, pca_board:PCABoard, memory:Memory, car_engine:CarEngine,
                 car_driver:CarDriver, car_eye:CarEye, running_ref):
        self.pca_board = pca_board
        self.carMemory = memory
        self.carEngine = car_engine
        self.carDriver = car_driver
        self.carEye = car_eye
        self.sensor_Board = MCP23017()
        self.current_angle = DRIVER_DEFAULT_ANGLE
        self.stuck = False
        self.last_max_angle = float()
        self.running_ref = running_ref
        self.time_array = deque(maxlen=6)
                
    def stuck_detection_logic(self):
        """This method detects if the car is stuck in the same movement seuence"""
        
        current_time = time.time()
        self.time_array.append(current_time)
        if len(self.time_array) == 6:
            A = self.time_array[5] - self.time_array[4]
            B = self.time_array[4] - self.time_array[3]
            C = self.time_array[3] - self.time_array[2]
            D = self.time_array[2] - self.time_array[1]
            E = self.time_array[1] - self.time_array[0]
            self.carMemory.log(
                                "info", f"Time Array:\n A:{A}\n B:{B}\n C:{C}\n D:{D}\n E:{E}")           
            if (abs(A - B) <= MAX_DIFF_TIME 
                and abs(B - C) <= MAX_DIFF_TIME 
                and abs(C - D) <= MAX_DIFF_TIME 
                and abs(D - E) <= MAX_DIFF_TIME):
                
                self.stuck = True
                self.carMemory.log(
                                "info", "The car is assumed to be stuck in the same position.")
            elif (abs(A - C) <= MAX_DIFF_TIME
                  and abs(C - E) <= MAX_DIFF_TIME 
                  and abs(B - D) <= MAX_DIFF_TIME):
                self.stuck = True
                self.carMemory.log(
                                "info", "The car is assumed to be stuck in the same position.")
            else:
                self.stuck = False
            
        return self.stuck
    
    def handle_stuck(self):
        """This is method 1 which handles the car when it is stuck in the same movement sequence"""
        self.carEngine.move_reverse(50)
        start_time = time.time()
        distance_back = self.sensor_Board.rear_ultrasonic.get_distance()
        while time.time() - start_time < 10 and distance_back > REAR_MINIMUM_GAP:
            distance_back = self.sensor_Board.rear_ultrasonic.get_distance()
            if not self.running_ref():
                self.carEngine.stop()
                return

        self.carEngine.stop()
        if self.last_max_angle != DRIVER_MAX_ANGLE:
            turning_angle = DRIVER_MAX_ANGLE
        else:
            turning_angle = DRIVER_MIN_ANGLE
            
        self.carDriver.set_front_angle(turning_angle)
        self.last_max_angle = turning_angle
        
        if turning_angle == DRIVER_MAX_ANGLE:
            self.carEye.set_angle(EYE_MIN_ANGLE)
        else:
            self.carEye.set_angle(EYE_MAX_ANGLE)
            
        self.carEngine.move_forward(MINIMUM_SPEED)
        
    