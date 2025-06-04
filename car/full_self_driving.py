import time
import math
import threading
from enum import Enum
from .memory import Memory
from .stuck_handler import StuckHandler
from .classes.car_eye import CarEye
from .classes.pca_board import PCABoard
from .classes.car_eye import MoveStatus
from .classes.car_engine import CarEngine
from .classes.car_driver import CarDriver
from .classes.ultrasonic_sensor import UltraSonicSensor
from .classes.class_config import EYE_MAX_ANGLE, DRIVER_DEFAULT_ANGLE, DRIVER_MAX_ANGLE, EYE_DEFAULT_ANGLE
from .car_config import (MINIMUM_SPEED,
                         MID_SPEED,
                         MAX_SPEED,
                         GEAR_INCRECEMENT_VALUE,
                         GEAR_SHIFTING_TIME,
                         REAR_MINIMUM_GAP,
                         EXTREME_MIN_GAP)


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
        self.ultraSonicSensor = UltraSonicSensor()
        self.stuckHandler = StuckHandler(
            self.pca_board, self.carMemory, self.carEngine, self.carDriver, self.carEye,
            running_ref=lambda: self.running)

        self.MID_SPEED = MID_SPEED
        self.MAX_SPEED = MAX_SPEED
        self.GEAR_INCRECEMENT_VALUE = GEAR_INCRECEMENT_VALUE

        self.running = False
        self.special_senario_handling = False
        self.moving = bool()
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
        self.carMemory.cleanup()

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
        eye_turning_angle = EYE_DEFAULT_ANGLE
        distance_front = self.carEye.get_distance_front()
        distance_back = self.ultraSonicSensor.get_distance()
        if distance_front <= MINIMUM_GAP and distance_back > REAR_MINIMUM_GAP:
            self.carEngine.stop()
            self.pca_board.reset()
            self.carEngine.move_reverse(50)
            while True:
                with self.lock:
                    if not self.running:
                        break
                distance_front = self.carEye.get_distance_front()
                distance_back = self.ultraSonicSensor.get_distance()
                if distance_front > MINIMUM_GAP:
                    break

                if distance_back < REAR_MINIMUM_GAP:
                    self.carEngine.stop()
                    self.pca_board.reset()
                    distance_front = self.carEye.get_distance_front()
                    distance_front, eye_turning_angle = self.carEye.get_the_direction_to_move(
                        EXTREME_MIN_GAP)
                    driver_eye_turning_angle = EYE_MAX_ANGLE - eye_turning_angle

                    while distance_front > EXTREME_MIN_GAP and eye_turning_angle != 0:
                        with self.lock:
                            if not self.running:
                                break
                        self.carDriver.set_front_angle(driver_eye_turning_angle)
                        self.carEye.set_angle(eye_turning_angle)
                        self.carEngine.move_forward(30)

                        distance_front = self.carEye.get_distance_front()
                    self.carEngine.stop()
                    self.pca_board.reset()
                    distance_front = self.carEye.get_distance_front()

                    if distance_front <= EXTREME_MIN_GAP:
                        distance_back = self.ultraSonicSensor.get_distance()
                        if distance_back > REAR_MINIMUM_GAP:
                            self.carEngine.stop()
                            self.pca_board.reset()
                            self.step_reverse(50)
                            while True:
                                with self.lock:
                                    if not self.running:
                                        break
                                distance_front = self.carEye.get_distance_front()
                                distance_back = self.ultraSonicSensor.get_distance()
                                if distance_back < REAR_MINIMUM_GAP:
                                    break
                    distance_front = self.carEye.get_distance_front()
                    if distance_front < MINIMUM_GAP:
                        self.carMemory.log(
                            "critical", "Manual assistance required to clear obstacles and resume operation.")

            self.carEngine.stop()
            distance_front, eye_turning_angle = self.carEye.get_the_direction_to_move(
                MINIMUM_GAP)
        return eye_turning_angle

    def smart_move_speed_front(self, current_speed, MINIMUM_GAP):
        move_status = self.carEye.can_i_keep_moving(MINIMUM_GAP)

        match move_status:
            case MoveStatus.Stop:
                target_speed = 0
                current_speed = 0
                return current_speed, target_speed

            case MoveStatus.Slow:
                target_speed = MINIMUM_SPEED
                if current_speed > MINIMUM_SPEED:
                    current_speed = max(
                        current_speed - 1, MINIMUM_SPEED)
                elif MINIMUM_SPEED > current_speed >= 0:
                    current_speed = min(
                        current_speed + 5, MINIMUM_SPEED)
                return current_speed, target_speed

            case MoveStatus.Maintain:
                target_speed = MID_SPEED
                if current_speed < MINIMUM_SPEED:
                    current_speed = min(
                        current_speed + 5, MINIMUM_SPEED)
                elif MINIMUM_SPEED <= current_speed < MID_SPEED:
                    current_speed = min(current_speed + 4, MID_SPEED)
                return current_speed, target_speed

            case MoveStatus.Accelerate:
                target_speed = MAX_SPEED
                if current_speed < MINIMUM_SPEED:
                    current_speed = min(current_speed + 5, MINIMUM_SPEED)
                elif MINIMUM_SPEED <= current_speed < MID_SPEED:
                    current_speed = min(current_speed + 1, MID_SPEED)
                elif MID_SPEED <= current_speed <= MAX_SPEED:
                    current_speed = min(current_speed + 1, MAX_SPEED)
                return current_speed, target_speed

        return current_speed, target_speed

    def smart_turn_driver_angle_back(self, current_angle, driver_turning_angle):
        return self.carDriver.get_rear_angle(current_angle, driver_turning_angle)

    def smart_turn_driver_angle_front(self, current_angle, driver_turning_angle):
        return self.carDriver.get_front_angle(current_angle, driver_turning_angle)

    def smart_turn_eye_angle_front(self, current_angle, eye_turning_angle):
        return self.carEye.get_front_angle(current_angle, eye_turning_angle)

    def default_values(self):
        current_eye_angle = EYE_DEFAULT_ANGLE
        eye_turning_angle = EYE_DEFAULT_ANGLE
        current_rear_angle = DRIVER_DEFAULT_ANGLE
        driver_rear_target = DRIVER_DEFAULT_ANGLE
        current_driver_angle = DRIVER_DEFAULT_ANGLE
        driver_turning_angle = DRIVER_DEFAULT_ANGLE
        return (current_eye_angle, eye_turning_angle,
                current_rear_angle, driver_rear_target,
                current_driver_angle, driver_turning_angle)
        
    def drive(self, MINIMUM_GAP):
        self.current_speed = 0
        self.target_speed = 0
        (current_eye_angle, eye_turning_angle,
        current_rear_angle, driver_rear_target,
        current_driver_angle, driver_turning_angle) = self.default_values()
        try:
            with self.lock:
                self.running = True
                self.carMemory.log(
                    "info", "Full Self-Driving Mode Activated, All Systems Intialized")
            while True:

                with self.lock:
                    if not self.running:
                        break

                self.current_speed, self.target_speed = self.smart_move_speed_front(
                    self.current_speed, MINIMUM_GAP)

                if self.target_speed == 0:
                    self.carEngine.stop()
                    self.pca_board.reset()
                    self.current_speed = 0
                    (current_eye_angle, eye_turning_angle,
                    current_rear_angle, driver_rear_target,
                    current_driver_angle, driver_turning_angle) = self.default_values()
                    
                    self.is_stuck = self.stuckHandler.stuck_detection_logic()
                    if self.is_stuck:
                        # This method will help to move the car ot of any stuck situation
                        self.stuckHandler.handle_stuck()
                        self.special_senario_handling = True

                    if not self.special_senario_handling:
                        distance = self.carEye.get_distance_front()
                        if distance <= MINIMUM_GAP:
                            eye_turning_angle = self.handle_cant_move_scenario(
                                MINIMUM_GAP)
                            if eye_turning_angle == 0:
                                self.turning = True
                                continue

                if current_driver_angle == driver_turning_angle and current_eye_angle == eye_turning_angle\
                        and current_rear_angle == driver_rear_target and self.current_speed >= MINIMUM_SPEED:
                    driver_turning_angle = DRIVER_DEFAULT_ANGLE
                    eye_turning_angle = EYE_DEFAULT_ANGLE
                    self.turning = False
                else:
                    self.turning = True

                if self.turning or (driver_turning_angle == DRIVER_DEFAULT_ANGLE and eye_turning_angle == EYE_DEFAULT_ANGLE):
                    driver_turning_angle = EYE_MAX_ANGLE - eye_turning_angle
                    current_driver_angle = self.smart_turn_driver_angle_front(
                    current_driver_angle, driver_turning_angle)
                    
                    current_eye_angle = self.smart_turn_eye_angle_front(
                    current_eye_angle, eye_turning_angle)

                if current_driver_angle != DRIVER_DEFAULT_ANGLE and current_eye_angle != EYE_DEFAULT_ANGLE:
                    self.carDriver.set_front_angle(current_driver_angle)
                    self.carEye.set_angle(current_eye_angle)
                    time.sleep(.5)

                if self.special_senario_handling:
                    self.current_speed = MID_SPEED
                    self.special_senario_handling = False
                self.carEngine.move_forward(self.current_speed)

        finally:
            self.carEngine.stop()
            self.pca_board.reset()
            self.cleanup()
            self.current_speed = 0
            (current_eye_angle,
            eye_turning_angle,
            current_rear_angle,
            driver_rear_target,
            current_driver_angle,
            driver_turning_angle) = self.default_values()


def run():
    self_drive = FullSelfDriving()
    self_drive.drive()
    time.sleep(5)
    self_drive.stop_loop()
