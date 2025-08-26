import re
import json
import logging
from datetime import datetime
from Car.config import (DRIVER_DEFAULT_ANGLE,
                        INFO_LOG_FILE_PATH,
                        ERROR_LOG_FILE_PATH
)
class Logger:
    def __init__(self):
        self.speed = 0.0
        self.angle = 25
        self.function = "Stopped"
        self.movement_sequence = []
        self.consecutive_repeats = int()
        self.threshold_repeats = 0
        self.errors = []
        self.last_function = "Stopped"
        self.last_angle = DRIVER_DEFAULT_ANGLE
        self.last_speed = 0
        self.logger = logging.getLogger('Self-Driving Car Memory')
        self.logger.setLevel(logging.DEBUG)


        if not any(isinstance(handler, logging.FileHandler) for handler in self.logger.handlers):
            self.debug_info_handler = logging.FileHandler(INFO_LOG_FILE_PATH)
            self.debug_info_handler.setLevel(logging.DEBUG)
            
            self.error_critical_handler = logging.FileHandler(ERROR_LOG_FILE_PATH)
            self.error_critical_handler.setLevel(logging.ERROR)

            log_formatter = logging.Formatter('%(levelname)s - %(message)s')

            self.debug_info_handler.setFormatter(log_formatter)
            self.error_critical_handler.setFormatter(log_formatter)

            self.logger.addHandler(self.debug_info_handler)
            self.logger.addHandler(self.error_critical_handler)

    def update_info(self, function, angle=None, speed=None):
        if speed is None:
            speed = self.speed
        if angle is None:
            angle = self.last_angle

        log_entry = {
            "Timestamp": datetime.now().isoformat(),
            "Function": function,
            "Angle": angle if angle is not None else self.angle,
            "Speed": speed,
        }
        if (self.last_function != function or self.last_angle != angle or self.last_speed != speed):
            self.logger.info(json.dumps(log_entry))
        self.last_function = function
        self.last_angle = angle
        self.last_speed = speed
        
    def log(self, type: str, message: str):
        type = type.lower()
        if type == "debug":
            self.logger.debug(message)
        elif type == "info":
            self.logger.info(message)
        elif type == "warning":
            self.logger.warning(message)
        elif type == "error":
            self.errors.append(message)
            self.logger.error(message)
        elif type == "exception":
            self.errors.append(message)
            self.logger.exception(message)
        elif type == "critical":
            self.errors.append(message)
            self.logger.critical(message)
        elif type == "log":
            self.logger.log(logging.INFO, message)
        else:
            self.logger.log(logging.INFO, message)
            
    def move_forward(self, speed):
        self.speed = speed
        self.function = "Move Forward"
        self.update_info(self.function, speed=self.speed)

    def move_backward(self, speed):
        self.speed = speed
        self.function = "Move Backward"
        self.update_info(self.function, speed=self.speed)
        
    def turn(self, angle):
        if angle > DRIVER_DEFAULT_ANGLE:
            self.function = "Turn Right"
            self.angle = int(angle - DRIVER_DEFAULT_ANGLE)
            
        elif DRIVER_DEFAULT_ANGLE > angle:
            self.function = "Turn Left"
            self.angle = int(DRIVER_DEFAULT_ANGLE - angle)
            
        self.update_info(function=self.function, angle=angle)
        
    def stop(self):
        self.function = "Stopped"
        self.update_info("Stopped", speed="0.0")
        self.speed = 0.0
        
    def cleanup(self):
        self.function = "Cleanup" 
        self.update_info("Cleanup", speed="0.0")
        self.log("info", "Self-Driving Car Deactivated, All Systems Shutting-Down -> Engine off")
    
    def eye_descition(self, array:list, choosed_angle:int, distance):
        self.function = "Eye Decision"
        self.log("info", f"Eye Array: {array} choosed angle: {choosed_angle} with distance: {distance*100} cm")
    

    def log_data(self):
        with open(INFO_LOG_FILE_PATH, "r") as log_file:
            log_content = log_file.readlines()
            return log_content
        
    def error_data(self):
        return self.errors