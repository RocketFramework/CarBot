import time
import random
import RPi.GPIO as GPIO
from car.car_config import MINIMUM_GAP

class UltrasonicSensor:
    def __init__(self, echo_pin, trigger_pin): # FIXME: This Code is a temporary mock code and does not return real values.
        self.distance = int()
        self.MINIMUM_GAP = MINIMUM_GAP
        self.echo_pin = echo_pin
        self.trigger_pin = trigger_pin

    def get_distance_to_obstacle(self):
        self.ditance = 0.88
        return self.distance

    def can_keep_moving(self):
        return False
     

    def cleanup(self):
        pass

if __name__ == "__main__":
    sensor = UltrasonicSensor(11, 17)
    gap = sensor.get_distance_to_obstacle()
    boolean = sensor.can_keep_moving()
    print(f"Distance To Obstacle = {gap}")
    print(f"Can move = {boolean}")
    sensor.cleanup()