from .car_config import  MINIMUM_GAP, WHEEL_RADIUS, ONE_WHEEL_TURN_LENGTH, ONE_WHEEL_TURN_STEPS
import math
import time
from typing import List
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.car_eye import CarEye

class FullSelfDriving:
    def __init__(self):
        self.carEngine = CarEngine()
        self.carDriver = CarDriver()
        self.carEye = CarEye()
        
    def drive(self):
        # 
        