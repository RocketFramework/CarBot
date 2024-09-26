from .servo_motor import Servo_Motor
from .class_config import TURN_ANGLE, DRIVER_SERVO_CONTROL_PIN, DRIVER_DEFAULT_ANGLE, DRIVER_MAX_ANGLE, DRIVER_MIN_ANGLE

class CarDriver:
    
    def __init__(self) -> None:
        self.current_angle = 0
        self.servo_motor = Servo_Motor(DRIVER_SERVO_CONTROL_PIN, DRIVER_DEFAULT_ANGLE)
    
    def turn_left(self) -> bool:
        self.current_angle = min(self.current_angle + TURN_ANGLE, DRIVER_MAX_ANGLE)
        self.servo_motor.rotate(self.current_angle)
        return self.current_angle < DRIVER_MAX_ANGLE
    
    def turn_right(self) -> bool:
        self.current_angle = max(self.current_angle - TURN_ANGLE, DRIVER_MIN_ANGLE)
        self.servo_motor.rotate(self.current_angle)
        return self.current_angle > DRIVER_MIN_ANGLE
    
    