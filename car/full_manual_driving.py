import time
import threading
from .classes.class_config import DRIVER_DEFAULT_ANGLE, DRIVER_MAX_ANGLE, DRIVER_MIN_ANGLE
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

        self.current_driver_angle = 25
        self.lock = threading.Lock()
        self.running = False
        self.direction = None
        self.drive_thread = None
        
    def move_forward(self, speed=50):
        self.carEngine.move_forward(speed)

    def reverse(self, speed=50):
        self.carEngine.move_reverse(speed)

    def turn_right(self, angle=5):
        if self.current_driver_angle < DRIVER_MAX_ANGLE:
            self.current_driver_angle += angle
        else:
            self.current_driver_angle = DRIVER_MAX_ANGLE
        self.carDriver.set_front_angle(self.current_driver_angle)
        return self.current_driver_angle

    def turn_left(self, angle=10):
        if self.current_driver_angle > DRIVER_MIN_ANGLE:
            self.current_driver_angle -= angle
        else:
            self.current_driver_angle = DRIVER_MIN_ANGLE
        self.carDriver.set_front_angle(self.current_driver_angle)
        return self.current_driver_angle

    def stop(self):
        with self.lock:
            self.running = False
        self.carEngine.stop()

    def cleanup(self):
        self.stop()
        self.pca_board.reset()
        self.carEngine.cleanup()

    def control_manualy(self):
        while self.running:
            with self.lock:
                if self.direction == "Forward" or self.direction == "Front":
                    self.move_forward()
                elif self.direction == "Reverse" or self.direction == "Back":
                    self.reverse()
                elif self.direction == "Right":
                    self.current_driver_angle = self.turn_right(self.current_driver_angle)
                elif self.direction == "Left":
                    self.current_driver_angle = self.turn_left(self.current_driver_angle)

            time.sleep(0.1)

    def drive(self, direction):
        with self.lock:
            self.direction = direction
            if not self.running:
                self.running = True
                self.drive_thread = threading.Thread(
                    target=self.control_manualy)
                self.drive_thread.start()


def run():
    driver = FullManualDriving()
    driver.drive("Forward")
    time.sleep(4)
    driver.drive("Reverse")
    time.sleep(4)
    driver.drive("Right")
    time.sleep(4)
    driver.drive("Left")
    time.sleep(4)
    driver.stop()
    driver.cleanup()
