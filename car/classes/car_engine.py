import time
from .dc_motor import DcMotor
from car.car_config import MAX_SPEED
class CarEngine:
    def __init__(self):
        self.dc_motor = DcMotor()
        self.car_speed = 0
        
    def move_forward(self, speed):
        self.car_speed = speed
        if self.car_speed < 0:
            self.dc_motor.set_motor_forward(0)
        elif self.car_speed > MAX_SPEED:
            self.dc_motor.set_motor_forward(MAX_SPEED)
        else:
            self.dc_motor.set_motor_forward(self.car_speed)
            
    def move_reverse(self, speed):
        self.car_speed = speed
        self.dc_motor.set_motor_reverse(speed)
      
    def stop(self):
        self.car_speed = 0
        self.dc_motor.stop_motor()
        
    def cleanup(self):
        """Cleanup GPIO settings when done."""
        self.dc_motor.cleanup()

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
