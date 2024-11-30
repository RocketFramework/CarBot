import time
import math
from .dc_motor import DcMotor
from car.car_config import MAX_SPEED, WHEEL_RADIUS, MAX_RPM

class CarEngine:
    def __init__(self):
        self.dc_motor = DcMotor()
        self.car_speed = 0
        self.WHEEL_RADIUS = WHEEL_RADIUS
        self.MAX_RPM = MAX_RPM  
        
    def speed_meter(self, percentage):
        rpm = (percentage / 100) * self.MAX_RPM
        return (2 * math.pi * self.WHEEL_RADIUS * rpm) / 60

    def move_forward(self, speed):
        self.car_speed = speed
        if self.car_speed < 0:
            self.car_speed = 0 
            self.dc_motor.set_motor_forward(0)
            speed = self.speed_meter(self.car_speed)
            print(f"Car Moving Forward at {self.car_speed}% Speed: {speed:.2f} m/s")
            
        elif self.car_speed > MAX_SPEED:
            self.dc_motor.set_motor_forward(MAX_SPEED)
            speed = self.speed_meter(self.car_speed)
            print(f"Car Moving Forward at {self.car_speed}% Speed: {speed:.2f} m/s")
            
        else:
            self.dc_motor.set_motor_forward(self.car_speed)
            speed = self.speed_meter(self.car_speed)
            print(f"Car Moving Forward at {self.car_speed}% Speed: {speed:.2f} m/s")
            
    def move_reverse(self, speed):
        self.car_speed = speed
        self.dc_motor.set_motor_reverse(speed)
        speed = self.speed_meter(self.car_speed)
        print(f"Car Moving Reverse at {self.car_speed}% Speed: {speed:.2f} m/s")
        
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
