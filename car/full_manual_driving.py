import time
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.car_eye import CarEye
from .classes.pca_board import PCABoard

class FullManualDriving:
    def __init__(self):
        self.pca_board = PCABoard()
        self.carEngine = CarEngine()
        self.carDriver = CarDriver(self.pca_board)
        self.carEye = CarEye(self.pca_board)
        
    def move_forward(self, speed):
        self.carEngine.move_forward(speed)
        
    def reverse(self, speed):
        self.carEngine.move_reverse(speed)
    
    def stop(self):
        self.carEngine.stop()
    
    def exit(self):
        self.carEngine.cleanup()

def run():  
    driver = FullManualDriving()
    driver.move_forward(50)
    time.sleep(5)

    driver.reverse(50)
    time.sleep(5)
    driver.stop()
    driver.exit()