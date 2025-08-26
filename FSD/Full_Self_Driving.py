import time
import math
import threading
from enum import Enum
from Car.__main__ import Car 
from Car.Units.Car_Eye import SpeedList
from LOG.Logger import Logger
from Car.config import (MINIMUM_SPEED,
                        MID_SPEED,
                        MAX_SPEED,
                        C_MINIMUM_GAP,
                        L_MINIMUM_GAP,
                        R_MINIMUM_GAP,
                        DRIVER_MAX_ANGLE,
                        REVERSE_SPEED,
                        MINIMUM_DISTANCE_BACK,
                        DRIVER_MIN_ANGLE,
                        DRIVER_DEFAULT_ANGLE,
                        EYE_MAX_ANGLE,
                        EYE_DEFAULT_ANGLE
                        
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
        self.running = False
        self.current_speed = int()
        self.lock = threading.Lock()
        self.target = Targets.Center
        self.processed = False
        self.reverse_dir = Targets.Center
        self.reverse_fail = False
        self.c_min_gap = C_MINIMUM_GAP
        self.l_min_gap = L_MINIMUM_GAP
        self.r_min_gap = R_MINIMUM_GAP
        self.intialised = True
        
    def smart_speed_control(self, L_MINIMUM_GAP, C_MINIMUM_GAP, R_MINIMUM_GAP):
        speedlist = self.Car.CarEye.smart_speed_monitor(L_MINIMUM_GAP, C_MINIMUM_GAP, R_MINIMUM_GAP)

        match speedlist:
            case SpeedList.Stop:
                self.current_speed = 0
                return self.current_speed

            case SpeedList.Slow:
                if self.current_speed > MINIMUM_SPEED:
                    self.current_speed = max(self.current_speed - 1, MINIMUM_SPEED)
                elif MINIMUM_SPEED > self.current_speed >= 0:
                    self.current_speed = min(self.current_speed + 5, MINIMUM_SPEED)
                return self.current_speed

            case SpeedList.Maintain:
                if self.current_speed < MINIMUM_SPEED:
                    self.current_speed = min(self.current_speed + 5, MINIMUM_SPEED)
                elif MINIMUM_SPEED <= self.current_speed < MID_SPEED:
                    self.current_speed = min(self.current_speed + 4, MID_SPEED)
                return self.current_speed

            case SpeedList.Accelerate:
                if self.current_speed < MINIMUM_SPEED:
                    self.current_speed = min(self.current_speed + 5, MINIMUM_SPEED)
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
        B = self.Car.sensor_board.rear_ultrasonic.get_distance()
        L, C, R = self.Car.CarEye.get_distance()
        
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
                current_driver_angle = current_angle -1
                
            elif current_angle < DRIVER_DEFAULT_ANGLE:
                current_driver_angle = current_angle +1
            else:
                current_driver_angle = DRIVER_DEFAULT_ANGLE
                
            return current_driver_angle
        else:
            return target_angle
    
    def smart_turn_eye(self, target_angle, current_angle):
        if target_angle == EYE_DEFAULT_ANGLE:
            if current_angle > EYE_DEFAULT_ANGLE:
                current_eye_angle = current_angle -1

            elif current_angle < EYE_DEFAULT_ANGLE:
                current_eye_angle = current_angle +1
            else:
                current_eye_angle = EYE_DEFAULT_ANGLE

            return current_eye_angle
        else:
            return target_angle
        
    def reset_values(self):
        currrent_driver_angle = DRIVER_DEFAULT_ANGLE
        current_eye_angle = EYE_DEFAULT_ANGLE
        driver_turning_angle = DRIVER_DEFAULT_ANGLE
        eye_turning_angle = EYE_DEFAULT_ANGLE   
        return currrent_driver_angle, driver_turning_angle, current_eye_angle, eye_turning_angle 
    
    def drive(self):
        try:
            with self.lock:
                self.running = True
                
            self.target = Targets.Center
            self.processed = False
            self.reverse_fail = False
            self.current_speed = 0
            C_MINIMUM_GAP = self.c_min_gap
            L_MINIMUM_GAP = self.l_min_gap
            R_MINIMUM_GAP = self.r_min_gap
            (currrent_driver_angle,
             driver_turning_angle,
             current_eye_angle,
             eye_turning_angle) = self.reset_values()
            
            while True:
                with self.lock:
                    if not self.running:
                        break

                current_speed = self.smart_speed_control(L_MINIMUM_GAP, C_MINIMUM_GAP, R_MINIMUM_GAP)
                if currrent_driver_angle == DRIVER_DEFAULT_ANGLE and current_eye_angle == EYE_DEFAULT_ANGLE:
                    driver_turning_angle, eye_turning_angle = self.smart_dir_calc(self.target)

                if self.processed and current_speed == 0:
                    self.Car.CarEngine.stop()
                    L, C, R = self.Car.CarEye.get_distance()
                    if L <= L_MINIMUM_GAP or C <= C_MINIMUM_GAP or R <= R_MINIMUM_GAP:
                        self.reverse_dir = self.smart_reverse_dir(self.target)
                        result = self.smart_reverse(self.reverse_dir, C_MINIMUM_GAP, L_MINIMUM_GAP, R_MINIMUM_GAP)

                        if result == Results.Fail:
                            self.reverse_fail = True
                            continue
                        
                        elif result == Results.Success:
                            self.reverse_fail = False
                            self.processed = False
                            C_MINIMUM_GAP = self.c_min_gap
                            L_MINIMUM_GAP = self.l_min_gap
                            R_MINIMUM_GAP = self.r_min_gap
                            self.target = Targets.Center
                            (currrent_driver_angle,
                            driver_turning_angle,
                            current_eye_angle,
                            eye_turning_angle) = self.reset_values()
                            _, eye_turning_angle = self.Car.CarEye.get_moving_direction()
                            driver_turning_angle = EYE_MAX_ANGLE - eye_turning_angle

                elif current_speed == 0:
                    self.processed = True
                    self.Car.CarEngine.stop()
                    L, C, R = self.Car.CarEye.get_distance()
                    self.logger.log("info", f"Distances - Left: {L}, Center: {C}, Right: {R}")
                    if L > L_MINIMUM_GAP and C <= C_MINIMUM_GAP and R > R_MINIMUM_GAP:
                        self.target = Targets.Reverse
                    
                    elif L > L_MINIMUM_GAP and C > C_MINIMUM_GAP and R > R_MINIMUM_GAP:
                        eye_turning_angle == self.Car.CarEye.get_moving_direction()
                        current_eye_angle = EYE_DEFAULT_ANGLE
                        
                    elif L <= L_MINIMUM_GAP and C <= C_MINIMUM_GAP and R <= R_MINIMUM_GAP:
                        self.target = Targets.Reverse  
                        
                    elif L <= L_MINIMUM_GAP and C > C_MINIMUM_GAP and R <= R_MINIMUM_GAP:
                        self.target = Targets.Reverse
                           
                    elif L <= L_MINIMUM_GAP and C > C_MINIMUM_GAP and R > R_MINIMUM_GAP:
                        self.target = Targets.Right
                        if L_MINIMUM_GAP > 0:
                            L_MINIMUM_GAP = L_MINIMUM_GAP/2
                        
                    elif L > L_MINIMUM_GAP and C > C_MINIMUM_GAP and R <= R_MINIMUM_GAP:
                        self.target = Targets.Left
                        if R_MINIMUM_GAP > 0:
                            R_MINIMUM_GAP = R_MINIMUM_GAP/2
                        
                    elif L <= L_MINIMUM_GAP and C <= C_MINIMUM_GAP and R > R_MINIMUM_GAP:
                        self.target = Targets.Right
                        if L_MINIMUM_GAP > 0:
                            L_MINIMUM_GAP = L_MINIMUM_GAP/2
                        if C_MINIMUM_GAP > 0:
                            C_MINIMUM_GAP = C_MINIMUM_GAP/2
                            
                    elif L > L_MINIMUM_GAP and C <= C_MINIMUM_GAP and R <= R_MINIMUM_GAP:
                        self.target = Targets.Left
                        if R_MINIMUM_GAP > 0:
                            R_MINIMUM_GAP = R_MINIMUM_GAP/2

   
                    else:
                        self.processed = False
                    
                else:
                    self.processed = False
                    
                if currrent_driver_angle == driver_turning_angle:
                    driver_turning_angle = DRIVER_DEFAULT_ANGLE
                    
                if current_eye_angle == eye_turning_angle:
                    eye_turning_angle = EYE_DEFAULT_ANGLE
                
                currrent_driver_angle = self.smart_turn_driver(driver_turning_angle, currrent_driver_angle)
                current_eye_angle = self.smart_turn_eye(eye_turning_angle, current_eye_angle)
                
                self.Car.move_forward(current_speed)        
                self.Car.CarEye.set_angle(current_eye_angle)
                self.Car.CarDriver.set_angle(1, currrent_driver_angle)


        finally:
            self.Car.stop()
            self.Car.cleanup()
            
    def stop(self):
        with self.lock:
            self.running = False
            self.processed = False
            self.reverse_fail = False
            self.target = Targets.Center
            self.current_speed = 0
            self.Car.stop()
            self.Car.cleanup()
            print("Full Self Driving stopped.")