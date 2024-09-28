from .classes.motor import Motor
from .classes.lida_sensor import LidarSensor
import time

class Telemetry:
    def __init__(self):
        self.sensor = LidarSensor()

    def gather_data(self):
        data = {
            'sensor_data': self.sensor.get_data(),
            'timestamp': time.time()
        }
        return data
