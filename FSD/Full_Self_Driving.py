import time
import math
import threading
from enum import Enum
from Car.__main__ import Car
from Car.Units.Car_Eye import SpeedList
from Car.Units.Car_Navigator import Car_Navigator
from Car.Handlers.stuck_handler import StuckHandler
from LOG.Logger import Logger
from Car.config import (MINIMUM_SPEED,
                        MID_SPEED,
                        MAX_SPEED,
                        REVERSE_SPEED,
                        C_MINIMUM_GAP,
                        L_MINIMUM_GAP,
                        R_MINIMUM_GAP,
                        EYE_MAX_ANGLE,
                        EYE_DEFAULT_ANGLE,
                        DRIVER_MIN_ANGLE,
                        DRIVER_MAX_ANGLE,
                        DRIVER_DEFAULT_ANGLE,
                        MINIMUM_DISTANCE_BACK,
                        MINIMUM_GAP_AVOID_RATE,
                        )


class Targets(Enum):
    Left = 0
    Center = 1
    Right = 2
    Reverse = 3


class Results(Enum):
    Fail = 0
    Success = 1


class FullSelfDriving:
    def __init__(self):
        self.logger = Logger()
        self.Car = Car(self.logger)
        self.Car_Navigator = Car_Navigator()
        self.StuckHandler = StuckHandler(self.Car)
        
        self.running = False
        self.processed = False
        self.reverse_fail = False
        self.current_speed = int()
        
        self.lock = threading.Lock()
        self.target = Targets.Center
        self.reverse_dir = Targets.Center
        
        self.C_MINIMUM_GAP = C_MINIMUM_GAP
        self.L_MINIMUM_GAP = L_MINIMUM_GAP
        self.R_MINIMUM_GAP = R_MINIMUM_GAP

    def smart_speed_control(self, L_MINIMUM_GAP, C_MINIMUM_GAP, R_MINIMUM_GAP):
        speedlist = self.Car.CarEye.smart_speed_monitor(
            L_MINIMUM_GAP, C_MINIMUM_GAP, R_MINIMUM_GAP)

        match speedlist:
            case SpeedList.Stop:
                self.current_speed = 0
                return self.current_speed

            case SpeedList.Slow:
                if self.current_speed > MINIMUM_SPEED:
                    self.current_speed = max(
                        self.current_speed - 1, MINIMUM_SPEED)
                elif MINIMUM_SPEED > self.current_speed >= 0:
                    self.current_speed = min(
                        self.current_speed + 5, MINIMUM_SPEED)
                return self.current_speed

            case SpeedList.Maintain:
                if self.current_speed < MINIMUM_SPEED:
                    self.current_speed = min(
                        self.current_speed + 5, MINIMUM_SPEED)
                elif MINIMUM_SPEED <= self.current_speed < MID_SPEED:
                    self.current_speed = min(self.current_speed + 4, MID_SPEED)
                return self.current_speed

            case SpeedList.Accelerate:
                if self.current_speed < MINIMUM_SPEED:
                    self.current_speed = min(
                        self.current_speed + 5, MINIMUM_SPEED)
                elif MINIMUM_SPEED <= self.current_speed < MID_SPEED:
                    self.current_speed = min(self.current_speed + 1, MID_SPEED)
                elif MID_SPEED <= self.current_speed <= MAX_SPEED:
                    self.current_speed = min(self.current_speed + 1, MAX_SPEED)
                return self.current_speed

        return self.current_speed

    def smart_reverse(self, reverse_dir, C_MINIMUM_GAP, L_MINIMUM_GAP, R_MINIMUM_GAP):
        angle = DRIVER_DEFAULT_ANGLE
        self.Car.stop()
        self.Car.pca_board.reset()
        L, C, R = self.Car.CarEye.get_distance()
        B = self.Car.sensor_board.rear_ultrasonic.get_distance() 

        if L <= L_MINIMUM_GAP or C <= C_MINIMUM_GAP or R <= R_MINIMUM_GAP:
            if reverse_dir == Targets.Left:
                angle = DRIVER_MAX_ANGLE
            elif reverse_dir == Targets.Right:
                angle = DRIVER_MIN_ANGLE
            elif reverse_dir == Targets.Center:
                angle = DRIVER_DEFAULT_ANGLE

            while B > MINIMUM_DISTANCE_BACK:
                self.Car.CarDriver.set_angle(1, angle)
                self.Car.move_reverse(REVERSE_SPEED)
                B = self.Car.sensor_board.rear_ultrasonic.get_distance()
                L, C, R = self.Car.CarEye.get_distance()
                if L > L_MINIMUM_GAP and C > C_MINIMUM_GAP and R > R_MINIMUM_GAP:
                    break

        self.Car.stop()
        self.Car.CarDriver.set_angle(1, DRIVER_DEFAULT_ANGLE)

        if L > L_MINIMUM_GAP or C > C_MINIMUM_GAP or R > R_MINIMUM_GAP:
            return Results.Success
        elif L <= L_MINIMUM_GAP or C <= C_MINIMUM_GAP or R <= R_MINIMUM_GAP:
            return Results.Fail

    def smart_dir_calc(self, target_dir):
        if target_dir == Targets.Left:
            driver_turning_angle = DRIVER_MIN_ANGLE
            eye_turning_angle = EYE_MAX_ANGLE - driver_turning_angle
            return driver_turning_angle, eye_turning_angle

        elif target_dir == Targets.Right:
            driver_turning_angle = DRIVER_MAX_ANGLE
            eye_turning_angle = EYE_MAX_ANGLE - driver_turning_angle
            return driver_turning_angle, eye_turning_angle

        elif target_dir == Targets.Center:
            driver_turning_angle = DRIVER_DEFAULT_ANGLE
            eye_turning_angle = EYE_MAX_ANGLE - driver_turning_angle
            return driver_turning_angle, eye_turning_angle

        return DRIVER_DEFAULT_ANGLE, EYE_MAX_ANGLE - DRIVER_DEFAULT_ANGLE

    def smart_reverse_dir(self, target_dir):
        return target_dir

    def smart_turn_driver(self, target_angle, current_angle):
        if target_angle == DRIVER_DEFAULT_ANGLE:
            if current_angle > DRIVER_DEFAULT_ANGLE:
                current_driver_angle = current_angle - 1

            elif current_angle < DRIVER_DEFAULT_ANGLE:
                current_driver_angle = current_angle + 1
                
            else:
                current_driver_angle = DRIVER_DEFAULT_ANGLE

            return current_driver_angle
        else:
            return target_angle

    def smart_turn_eye(self, target_angle, current_angle):
        if target_angle == EYE_DEFAULT_ANGLE:
            if current_angle > EYE_DEFAULT_ANGLE:
                current_eye_angle = current_angle - 1
                
            elif current_angle < EYE_DEFAULT_ANGLE:
                current_eye_angle = current_angle + 1
                
            else:
                current_eye_angle = EYE_DEFAULT_ANGLE

            return current_eye_angle
        else:
            return target_angle

    def reset_values(self):
        current_driver_angle = DRIVER_DEFAULT_ANGLE
        current_eye_angle = EYE_DEFAULT_ANGLE
        driver_turning_angle = DRIVER_DEFAULT_ANGLE
        eye_turning_angle = EYE_DEFAULT_ANGLE
        
        return (current_driver_angle,
                driver_turning_angle,
                current_eye_angle,
                eye_turning_angle)

    def drive(self):
        try:
            with self.lock:
                self.running = True

            self.current_speed = 0
            self.processed = False
            self.reverse_fail = False
            self.target = Targets.Center
      
            c_minimum_gap = self.C_MINIMUM_GAP
            l_minimum_gap = self.L_MINIMUM_GAP
            r_minimum_gap = self.R_MINIMUM_GAP
            
            (current_driver_angle,
             driver_turning_angle,
             current_eye_angle,
             eye_turning_angle) = self.reset_values()

            while True:
                with self.lock:
                    if not self.running:
                        break

                current_speed = self.smart_speed_control(
                    l_minimum_gap,
                    c_minimum_gap,
                    r_minimum_gap)
                
                if current_driver_angle == DRIVER_DEFAULT_ANGLE and current_eye_angle == EYE_DEFAULT_ANGLE:
                    driver_turning_angle, eye_turning_angle = self.smart_dir_calc(
                        self.target)

                if self.processed and current_speed == 0:
                    self.Car.CarEngine.stop()
                    stuck = self.Car_Navigator.stuck_detection_logic()
                    
                    if stuck:
                        self.logger.log(
                            "info", "The car is Stuck, Trying to avoid the loop.")
                        stuck_result = self.StuckHandler.method_1()
                        
                        if stuck_result == False:
                            self.logger.log(
                                "info", "Stuck Handler failed to resolve the issue, Re-evaluating the situation.")
                            continue
                        
                    L, C, R = self.Car.CarEye.get_distance()
                    
                    if L <= l_minimum_gap or C <= c_minimum_gap or R <= r_minimum_gap:
                        self.reverse_dir = self.smart_reverse_dir(self.target)
                        
                        result = self.smart_reverse(
                            self.reverse_dir, c_minimum_gap, l_minimum_gap, r_minimum_gap)

                        if result == Results.Fail:
                            self.reverse_fail = True

                            continue

                        elif result == Results.Success:
                            self.processed = False
                            self.reverse_fail = False
                            self.target = Targets.Center
                            
                            c_minimum_gap = self.C_MINIMUM_GAP
                            l_minimum_gap = self.L_MINIMUM_GAP
                            r_minimum_gap = self.R_MINIMUM_GAP
                            
                            (current_driver_angle,
                             driver_turning_angle,
                             current_eye_angle,
                             eye_turning_angle) = self.reset_values()
                            
                            _, eye_turning_angle = self.Car.CarEye.get_moving_direction()
                            driver_turning_angle = EYE_MAX_ANGLE - eye_turning_angle

                elif current_speed == 0:
                    
                    self.processed = True
                    self.Car.CarEngine.stop()
                    stuck = self.Car_Navigator.stuck_detection_logic()
                    
                    if stuck:
                        self.logger.log(
                            "info", "The car is Stuck, Trying to avoid the loop.")
                        stuck_result = self.StuckHandler.method_1()
                        
                        if stuck_result == False:
                            self.logger.log(
                                "info", "Stuck Handler failed to resolve the issue, Re-evaluating the situation.")
                            continue
                        
                    L, C, R = self.Car.CarEye.get_distance()
                    
                    self.logger.log(
                        "info", f"Distances - Left: {L}, Center: {C}, Right: {R}")
                    
                    if L > l_minimum_gap and C <= c_minimum_gap and R > r_minimum_gap:
                        self.target = Targets.Reverse

                    elif L > l_minimum_gap and C > c_minimum_gap and R > r_minimum_gap:
                        _, eye_turning_angle = self.Car.CarEye.get_moving_direction()
                        current_eye_angle = EYE_DEFAULT_ANGLE

                    elif L <= l_minimum_gap and C <= c_minimum_gap and R <= r_minimum_gap:
                        self.target = Targets.Reverse

                    elif L <= l_minimum_gap and C > c_minimum_gap and R <= r_minimum_gap:
                        self.target = Targets.Reverse

                    elif L <= l_minimum_gap and C > c_minimum_gap and R > r_minimum_gap:
                        self.target = Targets.Right
                        if l_minimum_gap > MINIMUM_GAP_AVOID_RATE:
                            l_minimum_gap = l_minimum_gap/2

                    elif L > l_minimum_gap and C > c_minimum_gap and R <= r_minimum_gap:
                        self.target = Targets.Left
                        if r_minimum_gap > MINIMUM_GAP_AVOID_RATE:
                            r_minimum_gap = r_minimum_gap/2

                    elif L <= l_minimum_gap and C <= c_minimum_gap and R > r_minimum_gap:
                        self.target = Targets.Right
                        if l_minimum_gap > MINIMUM_GAP_AVOID_RATE:
                            l_minimum_gap = l_minimum_gap/2
                        if c_minimum_gap > MINIMUM_GAP_AVOID_RATE:
                            c_minimum_gap = c_minimum_gap/2

                    elif L > l_minimum_gap and C <= c_minimum_gap and R <= r_minimum_gap:
                        self.target = Targets.Left
                        if r_minimum_gap > MINIMUM_GAP_AVOID_RATE:
                            r_minimum_gap = r_minimum_gap/2
                    else:
                        self.processed = False

                else:
                    self.processed = False

                if current_driver_angle == driver_turning_angle:
                    driver_turning_angle = DRIVER_DEFAULT_ANGLE

                if current_eye_angle == eye_turning_angle:
                    eye_turning_angle = EYE_DEFAULT_ANGLE

                current_driver_angle = self.Car_Navigator.smart_dir_calc(
                    driver_turning_angle)
                current_eye_angle = EYE_MAX_ANGLE - current_driver_angle

                self.Car.move_forward(current_speed)
                self.Car.CarEye.set_angle(current_eye_angle)
                self.Car.CarDriver.set_angle(1, current_driver_angle)

        finally:
            with self.lock:
                self.Car.stop()
                self.running = False
                self.processed = False
                self.reverse_fail = False
                self.target = Targets.Center

    def stop(self):
        with self.lock:
            self.current_speed = 0
            self.Car.stop()
            print("Full Self Driving stopped.")

    def cleanup(self):
        with self.lock:
            self.running = False
            self.processed = False
            self.reverse_fail = False
            self.target = Targets.Center
            self.Car.stop()
            self.Car.cleanup()
