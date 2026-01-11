import time
import threading
from enum import Enum
from Car.__main__ import Car
from Car.Units.Car_Eye import SpeedList
from Car.Handlers.stuck_handler import StuckHandler
from LOG.Logger import Logger
from Car.config import (
    MINIMUM_SPEED,
    MID_SPEED,
    MAX_SPEED,
    REVERSE_SPEED,
    C_MINIMUM_GAP,
    EYE_MAX_ANGLE,
    EYE_DEFAULT_ANGLE,
    DRIVER_MIN_ANGLE,
    DRIVER_MAX_ANGLE,
    DRIVER_DEFAULT_ANGLE,
    MINIMUM_DISTANCE_BACK,
    MINIMUM_GAP_AVOID_RATE,
)

class Targets(Enum):
    Center = 1
    Reverse = 3
    
class Results(Enum):
    Fail = 0
    Success = 1
    
class FullSelfDriving:
    def __init__(self):
        self.logger = Logger()
        self.Car = Car(self.logger)
        self.StuckHandler = StuckHandler(self.Car, running_ref=lambda: self.running)

        self.running = False
        self.processed = False
        self.reverse_fail = False
        self.current_speed = int()

        self.lock = threading.Lock()
        self.target = Targets.Center
        self.reverse_dir = Targets.Center

        self.C_MINIMUM_GAP = C_MINIMUM_GAP

        # Shared distance for threading
        self.distance = 0
        self.sensor_thread = None

    # ---------------------- SENSOR THREAD ----------------------
    def update_distance(self):
        while self.running:
            # Get only center distance
            _, C, _ = self.Car.CarEye.get_distance()
            with self.lock:
                self.distance = C
            time.sleep(0.02)  # ~50 Hz updates

    # ---------------------- SPEED CONTROL ----------------------
    def smart_speed_control(self, C_MINIMUM_GAP):
        with self.lock:
            C = self.distance
        
        # Simple proportional speed control
        if C <= C_MINIMUM_GAP:
            self.current_speed = 0
            return SpeedList.Stop
            
        elif C <= C_MINIMUM_GAP * 2:
            # Reduce speed proportionally to distance
            speed_reduction = int((C_MINIMUM_GAP * 2 - C) / C_MINIMUM_GAP * MINIMUM_SPEED)
            self.current_speed = max(MINIMUM_SPEED - speed_reduction, 0)
            return SpeedList.Slow if self.current_speed > 0 else SpeedList.Stop
            
        elif C <= C_MINIMUM_GAP * 4:
            self.current_speed = MINIMUM_SPEED
            return SpeedList.Maintain
            
        else:
            # Increase speed gradually
            if self.current_speed < MID_SPEED:
                self.current_speed = min(self.current_speed + 2, MID_SPEED)
            elif self.current_speed < MAX_SPEED:
                self.current_speed = min(self.current_speed + 1, MAX_SPEED)
            return SpeedList.Accelerate

    # ---------------------- REVERSE ----------------------
    def smart_reverse(self, C_MINIMUM_GAP):
        self.Car.stop()
        self.Car.pca_board.reset()
        
        # Get distances
        _, C, _ = self.Car.CarEye.get_distance()

        B = 150
        # Only reverse if center sensor detects obstacle
        if C <= C_MINIMUM_GAP:
            # Reverse straight back
            angle = DRIVER_DEFAULT_ANGLE
            
            # Reverse until enough space behind OR obstacle in front clears
            while B > MINIMUM_DISTANCE_BACK:
                self.Car.CarDriver.set_angle(1, angle)
                self.Car.move_reverse(REVERSE_SPEED)
                B = 150
                _, C, _ = self.Car.CarEye.get_distance()
                
                # Stop reversing if front obstacle clears
                if C > C_MINIMUM_GAP:
                    break

        self.Car.stop()
        self.Car.CarDriver.set_angle(1, DRIVER_DEFAULT_ANGLE)

        # Check if reversal was successful
        _, C, _ = self.Car.CarEye.get_distance()
        if C > C_MINIMUM_GAP:
            return Results.Success
        else:
            return Results.Fail

    # ---------------------- TURN CALC ----------------------
    def smart_dir_calc(self, target_dir):
        # With only center sensor, we can only go straight or reverse
        if target_dir == Targets.Center:
            driver_turning_angle = DRIVER_DEFAULT_ANGLE
            eye_turning_angle = EYE_MAX_ANGLE - driver_turning_angle
            return driver_turning_angle, eye_turning_angle
        return DRIVER_DEFAULT_ANGLE, EYE_MAX_ANGLE - DRIVER_DEFAULT_ANGLE

    def reset_values(self):
        return DRIVER_DEFAULT_ANGLE, DRIVER_DEFAULT_ANGLE, EYE_DEFAULT_ANGLE, EYE_DEFAULT_ANGLE

    # ---------------------- DRIVE ----------------------
    def drive(self):
        try:
            with self.lock:
                self.running = True

            self.current_speed = 0
            self.processed = False
            self.reverse_fail = False
            self.target = Targets.Center

            c_minimum_gap = int(self.C_MINIMUM_GAP)

            current_driver_angle, driver_turning_angle, current_eye_angle, eye_turning_angle = self.reset_values()

            # Start sensor thread
            self.sensor_thread = threading.Thread(target=self.update_distance, daemon=True)
            self.sensor_thread.start()

            while True:
                with self.lock:
                    if not self.running:
                        break
                    C = self.distance

                # Control speed based on center distance
                speed_result = self.smart_speed_control(c_minimum_gap)
                current_speed = self.current_speed

                # Reset turning angles to straight ahead (center only)
                if current_driver_angle == DRIVER_DEFAULT_ANGLE and current_eye_angle == EYE_DEFAULT_ANGLE:
                    driver_turning_angle, eye_turning_angle = self.smart_dir_calc(self.target)

                # Handle obstacle detection
                if self.processed and current_speed == 0:
                    self.Car.CarEngine.stop()
                    
                    # Check if stuck
                    stuck = False  # You'll need to implement stuck detection with single sensor
                    if stuck:
                        self.logger.log("info", "The car is Stuck, Trying to avoid the loop.")
                        stuck_result = self.StuckHandler.method_1()
                        if not stuck_result:
                            self.logger.log("info", "Stuck Handler failed to resolve the issue, Re-evaluating the situation.")
                            continue

                    # If center sensor detects obstacle
                    if C <= c_minimum_gap:
                        result = self.smart_reverse(c_minimum_gap)
                        if result == Results.Fail:
                            self.reverse_fail = True
                            continue
                        elif result == Results.Success:
                            self.processed = False
                            self.reverse_fail = False
                            self.target = Targets.Center
                            c_minimum_gap = self.C_MINIMUM_GAP
                            current_driver_angle, driver_turning_angle, current_eye_angle, eye_turning_angle = self.reset_values()
                            _, eye_turning_angle = self.Car.CarEye.get_moving_direction()
                            driver_turning_angle = EYE_MAX_ANGLE - eye_turning_angle

                elif current_speed == 0:
                    self.processed = True
                    self.Car.CarEngine.stop()
                    
                    # Check if stuck
                    stuck = False
                    if stuck:
                        self.logger.log("info", "The car is Stuck, Trying to avoid the loop.")
                        stuck_result = self.StuckHandler.method_1()
                        if not stuck_result:
                            self.logger.log("info", "Stuck Handler failed to resolve the issue, Re-evaluating the situation.")
                            continue

                    self.logger.log("info", f"Center Distance: {C}")
                else:
                    self.processed = False

                # Reset turning angles when reached
                if current_driver_angle == driver_turning_angle:
                    driver_turning_angle = DRIVER_DEFAULT_ANGLE
                if current_eye_angle == eye_turning_angle:
                    eye_turning_angle = EYE_DEFAULT_ANGLE

                # Simple straight-line driving
                current_driver_angle = DRIVER_DEFAULT_ANGLE
                current_eye_angle = EYE_MAX_ANGLE - current_driver_angle

                # Move vehicle
                self.Car.move_forward(current_speed)
                self.Car.CarEye.set_angle(current_eye_angle)
                self.Car.CarDriver.set_angle(1, current_driver_angle)

        finally:
            with self.lock:
                self.running = False
                self.Car.stop()
                self.processed = False
                self.reverse_fail = False
                self.target = Targets.Center

    # ---------------------- STOP & CLEANUP ----------------------
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