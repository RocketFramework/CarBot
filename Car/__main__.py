from Car.Units.Car_Engine import CarEngine
from Car.Units.Car_Driver import CarDriver
from Car.Units.Car_Navigator import Car_Navigator
from Car.Units.Car_Eye import CarEye
from Car.Hardware.pca_board import PCA9685
from Car.Hardware.mcp_board import MCP23017

class Car:
    def __init__(self, logger):
        self.logger = logger
        self.navigator = Car_Navigator()
        self.pca_board = PCA9685()
        self.engine = CarEngine(self.logger)
        self.driver = CarDriver(self.pca_board, self.logger)
        self.eye = CarEye(self.pca_board, self.logger)
        self.sensor_board = MCP23017()

    def move_forward(self, speed):
        self.engine.move_forward(speed)
    
    def move_reverse(self, speed):
        self.engine.move_reverse(speed)
        
    def stop(self):
        self.engine.stop()
    
    def cleanup(self):
        self.engine.cleanup()
        self.pca_board.reset()

    
    @property
    def CarDriver(self):
        return self.driver
    
    @property
    def CarEngine(self):
        return self.engine
    @property
    def CarRear(self):
        return self.rear

    @property
    def CarEye(self):
        return self.eye

    @property
    def CarSensor(self):
        return self.sensor_board

    @property
    def CarNavigator(self):
        return self.navigator