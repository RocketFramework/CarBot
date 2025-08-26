from Car.config import DRIVER_DEFAULT_ANGLE, EYE_DEFAULT_ANGLE, TURN_STEP_SIZE
from Car.Hardware.pca_board import PCA9685

class CarDriver:
    def __init__(self, pca_board, logger) -> None:
        self.front_servo = pca_board.driver_servo
        self.rear_servo = pca_board.rear_servo
        self.current_front_angle = self.front_servo.angle
        self.current_rear_angle = self.rear_servo.angle
        self.logger = logger
        
    def set_angle(self, id:int, angle:int):
        if id == 1:
            self.current_front_angle = self.front_servo.rotate(angle)
            self.logger.turn(angle)
            
        elif id == 2:
            self.current_rear_angle = self.rear_servo.rotate(angle)
            
    def smart_straight(self, current_angle:int, turning_angle:int):
        if turning_angle == DRIVER_DEFAULT_ANGLE:
            if turning_angle > current_angle:
                current_angle = int(current_angle + TURN_STEP_SIZE)
                return current_angle

            elif turning_angle < current_angle:
                current_angle = int(current_angle - TURN_STEP_SIZE)

                return current_angle

            return current_angle
        else:
            return turning_angle
        