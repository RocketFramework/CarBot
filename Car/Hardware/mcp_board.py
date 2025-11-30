import time
import board
import digitalio
import busio
from enum import Enum
from adafruit_mcp230xx.mcp23017 import MCP23017 as AdafruitMCP23017

from Car.Hardware.ultrasonic_sensor import UltraSonicSensor
from Car.config import EDGE_SENSOR_L_ECHO_PIN, EDGE_SENSOR_R_ECHO_PIN, ULTRASONIC_ECHO_PIN


class UltraSonicIds(Enum):
    REAR = 0
    LEFT = 1
    RIGHT = 2


class MCP23017:
    def __init__(self):
        self.I2C = busio.I2C(board.SCL, board.SDA)
        self.board = AdafruitMCP23017(self.I2C)
        self.REAR_TRIG = 17
        self.LEFT_EDGE_TRIG = 5
        self.RIGHT_EDGE_TRIG = 22

        self.REAR_ECHO = 1
        self.LEFT_EDGE_ECHO = 27
        self.RIGHT_EDGE_ECHO = 6


        self._REAR_ULTRASONIC = UltraSonicSensor(trigger_pin=self.REAR_TRIG,
                                                 echo_pin=self.REAR_ECHO)

        self._LEFT_EDGE_SENSOR = UltraSonicSensor(trigger_pin=self.LEFT_EDGE_TRIG,
                                                                         echo_pin=self.LEFT_EDGE_ECHO)

        self._RIGHT_EDGE_SENSOR = UltraSonicSensor(trigger_pin=self.RIGHT_EDGE_TRIG,
                                                   echo_pin=self.RIGHT_EDGE_ECHO)

    @property
    def rear_ultrasonic(self):
        return self._REAR_ULTRASONIC

    @property
    def left_edge_sensor(self):
        return self._LEFT_EDGE_SENSOR

    @property
    def right_edge_sensor(self):
        return self._RIGHT_EDGE_SENSOR

    def get_distance(self, sensor_id: UltraSonicIds):
        if sensor_id == UltraSonicIds.REAR:
            return self._REAR_ULTRASONIC.get_distance()
        elif sensor_id == UltraSonicIds.LEFT:
            return self._LEFT_EDGE_SENSOR.get_distance()
        elif sensor_id == UltraSonicIds.RIGHT:
            return self._RIGHT_EDGE_SENSOR.get_distance()
        else:
            raise ValueError("Invalid sensor ID")

    def get_min_distance(self):
        distance_L = self.left_edge_sensor.get_distance()
        distance_R = self.right_edge_sensor.get_distance()
        return min(distance_L, distance_R)
        
def run():
    mcp_sensors = MCP23017()
    try:
        x = 0
        
        while True:
            print(f"L:{mcp_sensors.left_edge_sensor.get_distance()} cm | R:{mcp_sensors.right_edge_sensor.get_distance()} cm | B:{mcp_sensors.rear_ultrasonic.get_distance()} cm")
            time.sleep(.5)
    except KeyboardInterrupt:
        print(x)
        print("Stopped.")
    finally:
        import RPi.GPIO as GPIO
        GPIO.cleanup()