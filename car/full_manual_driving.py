import time
import threading
from .classes.class_config import DRIVER_DEFAULT_ANGLE, DRIVER_MAX_ANGLE, DRIVER_MIN_ANGLE
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.car_eye import CarEye
from .classes.pca_board import PCABoard
from .memory import Memory


class FullManualDriving:
    def __init__(self):
        self.pca_board = PCABoard()
        self.carMemory = Memory()
        self.carEngine = CarEngine(self.carMemory)
        self.carDriver = CarDriver(self.pca_board, self.carMemory)
        self.carEye = CarEye(self.pca_board)

        self.current_driver_angle = DRIVER_DEFAULT_ANGLE
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
        if self.drive_thread and self.drive_thread.is_alive():
            self.drive_thread.join()  # Wait for thread to complete
        self.pca_board.reset()
        self.carEngine.cleanup()

    def control_manualy(self):
        while self.running:
            try:
                with self.lock:
                    if not self.running:
                        break
                    if self.direction.lower() in {"forward", "front"}:
                        self.move_forward()
                    elif self.direction.lower() in {"reverse", "back"}:
                        self.reverse()
                    elif self.direction.lower() == "right":
                        self.current_driver_angle = self.turn_right()
                    elif self.direction.lower() == "left":
                        self.current_driver_angle = self.turn_left()

                time.sleep(0.1)
            except Exception as e:
                print(f"Error in manual control: {e}")
                break
            finally:
                self.stop()

    def drive(self, direction):
        with self.lock:
            self.running = False  # Stop the current thread if running
        if self.drive_thread and self.drive_thread.is_alive():
            self.drive_thread.join()  # Wait for the thread to finish

        self.direction = direction
        self.running = True
        self.drive_thread = threading.Thread(target=self.control_manualy)
        self.drive_thread.start()


def run():
    driver = FullManualDriving()
    try:
        driver.drive("Forward")
        time.sleep(4)
        driver.stop()

        driver.drive("Reverse")
        time.sleep(4)
        driver.stop()

        driver.drive("Right")
        time.sleep(2)
        driver.stop()

        driver.drive("Left")
        time.sleep(2)
        driver.stop()
    finally:
        driver.cleanup()