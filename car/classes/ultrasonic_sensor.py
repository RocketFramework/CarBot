import time
import random
import RPi.GPIO as GPIO
from car.car_config import Minimum_Gap

class UltrasonicSensor:
    def __init__(self, echo_pin, trigger_pin): # FIXME: This Code is a temporary mock code and does not return real values.
        self.distance = int()
        self.MINIMUM_GAP = Minimum_Gap
        self.echo_pin = echo_pin
        self.trigger_pin = trigger_pin
        
    def get_distance_to_obstacle(self):
        self.ditance = round(random.uniform(1.5, 5.5), 2)
        return self.distance
    
    def can_keep_moving(self):
        time.sleep(0.001)
        self.ditance = self.get_distance_to_obstacle()
        if self.distance > self.MINIMUM_GAP:
            return True
        else:
            return False
    def cleanup(self):
        GPIO.cleanup()
    
        