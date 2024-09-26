from .class_config import EYE_SERVO_CONTROL_PIN, EYE_DEFAULT_ANGLE
from .car_driver import CarDriver
from .servo_motor import Servo_Motor
# Subclass (CarEye)
class CarEye(CarDriver):
    
    def __init__(self):
        # Custom initialization for CarEye, no call to super().__init__()
        self.current_angle = 0
        self.servo_motor = Servo_Motor(EYE_SERVO_CONTROL_PIN, EYE_DEFAULT_ANGLE)
    
    # The subclass will still inherit the turn_left() and turn_right() methods