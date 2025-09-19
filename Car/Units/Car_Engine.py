import time
import math
from Car.Hardware.dc_motor import DcMotor
from Car.config import MAX_SPEED, FRONT_RPWM_PIN, FRONT_LPWM_PIN, FRONT_REN_PIN, FRONT_LEN_PIN, REAR_RPM_PIN, REAR_LPWM_PIN, REAR_REN_PIN, REAR_LEN_PIN
class CarEngine:
    def __init__(self, logger):
        self.dc_motor_front = DcMotor(FRONT_RPWM_PIN, FRONT_LPWM_PIN, FRONT_REN_PIN, FRONT_LEN_PIN)
        self.dc_motor_rear = DcMotor(REAR_RPM_PIN, REAR_LPWM_PIN, REAR_REN_PIN, REAR_LEN_PIN)
        self.logger = logger
        self.car_speed = int()

    def move_forward(self, speed:int):
        self.car_speed = speed
        self.dc_motor_front.set_motor_forward(speed)
        self.dc_motor_rear.set_motor_forward(speed)
        self.logger.move_forward(speed)
        print(f"Car Moving Forward at {self.car_speed}% Speed")
            
    def move_reverse(self, speed):
        self.car_speed = speed
        self.dc_motor_front.set_motor_reverse(speed)
        self.dc_motor_rear.set_motor_reverse(speed)
        self.logger.move_backward(speed)
        print(f"Car Moving Reverse at {self.car_speed}% Speed")
        
    def stop(self):
        self.dc_motor_front.stop_motor()
        self.dc_motor_rear.stop_motor()
        self.logger.stop()
    def cleanup(self):
        """Cleanup GPIO settings when done."""
        self.dc_motor_front.cleanup()
        self.dc_motor_rear.cleanup()
        self.logger.cleanup()
def run():
    try:
        car = CarEngine()
        car.move_forward(100)
        time.sleep(100)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        car.stop()
        car.cleanup()