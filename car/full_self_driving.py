import time
import threading
from enum import Enum
from .memory import Memory
from .classes.car_eye import CarEye
from .classes.pca_board import PCABoard
from .classes.car_eye import MoveStatus
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.ultrasonic_sensor import UltrasonicSensor
from .classes.class_config import EYE_MAX_ANGLE, DRIVER_DEFAULT_ANGLE, EYE_DEFAULT_ANGLE
from .car_config import MINIMUM_SPEED, MID_SPEED, MAX_SPEED, REVERSE_SPEED, GEAR_SHIFTING_TIME, GEAR_INCRECEMENT_VALUE, REVERSE_SLEEP_TIME, HIGH_GAP, MID_GAP


class FullSelfDriving:
    """
    Full Self-Driving Function:
    Autonomously navigates the vehicle and reaches the destination safely.
    For Example, try FullselfDriving.drive(0.5)
    """

    def __init__(self):
        self.pca_board = PCABoard()
        self.carMemory = Memory()
        self.carEngine = CarEngine(self.carMemory)
        self.carDriver = CarDriver(self.pca_board, self.carMemory)
        self.carEye = CarEye(self.pca_board)
        self.ultrasonicSensor = UltrasonicSensor(1, 1.9)

        self.MID_SPEED = MID_SPEED
        self.MAX_SPEED = MAX_SPEED
        self.GEAR_INCRECEMENT_VALUE = GEAR_INCRECEMENT_VALUE

        self.running = False
        self.turning = bool()
        self.starting = bool()
        self.systemState = str()
        self.target_speed = int()
        self.current_speed = int()
        self.lock = threading.Lock()

    def stop_loop(self):
        with self.lock:
            self.running = False

    def cleanup(self):
        self.carEngine.cleanup()

    def calculate_rear_angle(self, front_angle: int) -> int:
        angle_diff = abs(front_angle - DRIVER_DEFAULT_ANGLE)
        if front_angle > DRIVER_DEFAULT_ANGLE:
            rear_angle = DRIVER_DEFAULT_ANGLE - (angle_diff // 2)
        elif front_angle < DRIVER_DEFAULT_ANGLE:
            rear_angle = DRIVER_DEFAULT_ANGLE + (angle_diff // 2)
        else:
            rear_angle = DRIVER_DEFAULT_ANGLE
        return rear_angle

    def handle_cant_move_scenario(self, MINIMUM_GAP):
        moving_angle = EYE_DEFAULT_ANGLE
        distance = self.carEye.get_distance_front()
        if distance <= MINIMUM_GAP:
            self.carEngine.stop()
            self.pca_board.reset()
            self.step_reverse(50)
            while True:
                with self.lock:
                    if not self.running:
                        break
                distance = self.carEye.get_distance_front()
                if distance > MINIMUM_GAP:
                    break

            self.carEngine.stop()
            distance, moving_angle = self.carEye.get_the_direction_to_move(
                MINIMUM_GAP)

        return moving_angle

    def reverse(self, speed):
        self.carEngine.move_reverse(speed)

    def step_reverse(self, speed):
        self.carEngine.move_reverse(speed)

    def smart_move_speed_front(self, current_speed, MINIMUM_GAP):
        if current_speed > 20:
            move_status = self.carEye.can_i_keep_moving(MID_GAP)
        else:
            move_status = self.carEye.can_i_keep_moving(MINIMUM_GAP)
        time.sleep(GEAR_SHIFTING_TIME)
        match move_status:
            case MoveStatus.Stop:
                target_speed = 0
                current_speed = 0
                return current_speed, target_speed

            case MoveStatus.Slow:
                target_speed = MINIMUM_SPEED
                if current_speed > MINIMUM_SPEED:
                    current_speed = max(
                        current_speed - self.GEAR_INCRECEMENT_VALUE, MINIMUM_SPEED)
                elif 20 > current_speed >= 0:
                    current_speed = min(
                        current_speed + self.GEAR_INCRECEMENT_VALUE, MINIMUM_SPEED)
                return current_speed, target_speed

            case MoveStatus.Maintain:
                target_speed = MID_SPEED
                if current_speed < 20:
                    current_speed = min(
                        current_speed + self.GEAR_INCRECEMENT_VALUE, MINIMUM_SPEED)
                elif 20 <= current_speed < MID_SPEED:
                    current_speed = min(current_speed + 2, MID_SPEED)
                return current_speed, target_speed

            case MoveStatus.Accelerate:
                target_speed = MAX_SPEED
                if current_speed < MINIMUM_SPEED:
                    current_speed = min(current_speed + 2, 50)
                elif MINIMUM_SPEED <= current_speed < MID_SPEED:
                    current_speed = min(current_speed + 5, MAX_SPEED)
                elif MID_SPEED <= current_speed <= MAX_SPEED:
                    current_speed = min(current_speed + 10, MAX_SPEED)
                return current_speed, target_speed

        return current_speed, target_speed

    def smart_turn_driver_angle_back(self, current_angle, driver_turning_angle):
        if driver_turning_angle == current_angle:
            current_angle = DRIVER_DEFAULT_ANGLE
            return DRIVER_DEFAULT_ANGLE

        return self.carDriver.get_rear_angle(current_angle, driver_turning_angle)

    def smart_turn_driver_angle_front(self, current_angle, driver_turning_angle):
        if driver_turning_angle == current_angle:
            current_angle = DRIVER_DEFAULT_ANGLE
            return DRIVER_DEFAULT_ANGLE

        return self.carDriver.get_front_angle(current_angle, driver_turning_angle)

    def smart_turn_eye_angle_front(self, current_angle, eye_turning_angle):
        if eye_turning_angle == current_angle:
            current_angle = EYE_DEFAULT_ANGLE
            return EYE_DEFAULT_ANGLE

        return self.carEye.get_front_angle(current_angle, eye_turning_angle)

    def drive(self, MINIMUM_GAP):       
        self.current_speed = 0
        self.target_speed = 0
        current_rear_angle = DRIVER_DEFAULT_ANGLE
        driver_rear_target = DRIVER_DEFAULT_ANGLE
        current_driver_angle = DRIVER_DEFAULT_ANGLE
        current_eye_angle = EYE_DEFAULT_ANGLE
        driver_turning_angle = DRIVER_DEFAULT_ANGLE
        eye_turning_angle = EYE_DEFAULT_ANGLE
        try:
            with self.lock:
                self.running = True

            while True:

                with self.lock:
                    if not self.running:
                        break

                self.current_speed, self.target_speed = self.smart_move_speed_front(
                    self.current_speed, MINIMUM_GAP)
                if self.target_speed == 0:
                    self.carEngine.stop()
                    self.pca_board.reset()
                    current_rear_angle = DRIVER_DEFAULT_ANGLE
                    current_driver_angle = DRIVER_DEFAULT_ANGLE
                    current_eye_angle = EYE_DEFAULT_ANGLE
                    self.current_speed = 0
                    distance = self.carEye.get_distance_front()
                    if distance <= MINIMUM_GAP:
                        eye_turning_angle = self.handle_cant_move_scenario(
                            MINIMUM_GAP)
                    
                        if eye_turning_angle == 0:
                            self.turning = True
                            continue

                elif self.target_speed == 20:
                    if self.current_speed == 20:
                        current_rear_angle = DRIVER_DEFAULT_ANGLE

                    if not self.turning:
                        distance, moving_angle = self.carEye.get_the_direction_to_move(
                            MINIMUM_GAP)
                        if moving_angle == 0:
                            self.carMemory.log(
                                "critical", "Manual assistance required to clear obstacles and resume operation.")
                            continue

                        eye_turning_angle = moving_angle

                    if current_driver_angle == driver_turning_angle and current_eye_angle == eye_turning_angle and current_rear_angle == driver_rear_target:
                        current_rear_angle = DRIVER_DEFAULT_ANGLE
                        driver_rear_target = DRIVER_DEFAULT_ANGLE
                        current_driver_angle = DRIVER_DEFAULT_ANGLE
                        current_eye_angle = EYE_DEFAULT_ANGLE
                        driver_turning_angle = DRIVER_DEFAULT_ANGLE
                        eye_turning_angle = EYE_DEFAULT_ANGLE
                        self.turning = False

                    else:
                        self.turning = True
                if self.turning:
                    eye_turning_angle = moving_angle
                    driver_turning_angle = EYE_MAX_ANGLE - eye_turning_angle
                    current_driver_angle = self.smart_turn_driver_angle_front(
                        current_driver_angle, driver_turning_angle)
                    current_eye_angle = self.smart_turn_eye_angle_front(
                        current_eye_angle, eye_turning_angle)

                self.carEngine.move_forward(self.current_speed)
                self.carEye.set_angle(current_eye_angle)
                self.carDriver.set_front_angle(current_driver_angle)
                self.carDriver.set_rear_angle(current_rear_angle)

        finally:
            self.carEngine.stop()
            self.pca_board.reset()
            self.current_speed = 0
            current_driver_angle = DRIVER_DEFAULT_ANGLE
            current_eye_angle = EYE_DEFAULT_ANGLE


def run():
    self_drive = FullSelfDriving()
    self_drive.drive()
    time.sleep(5)
    self_drive.stop_loop()
