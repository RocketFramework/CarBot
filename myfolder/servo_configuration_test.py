import time
from adafruit_servokit import ServoKit
# Initialize the PCA9685 board (16 channels)
kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 150
kit.servo[14].actuation_range = 150
# Test each channel to see if a motor/servo is connected

DRIVER_DEFAULT_ANGLE = 25
DRIVER_MIN_ANGLE = 0
DRIVER_MAX_ANGLE = 50
DRIVER_ACTUATION_RANGE = 150
DRIVER_CHANNEL = 14

TURN_STEP_SIZE = 1  # TODO: Calibrate turn step size

# Eye servo motor settings
EYE_MAX_ANGLE = 117
EYE_MIN_ANGLE = 67
EYE_ACTUATION_RANGE = 150
EYE_CHANNEL = 0
EYE_DEFAULT_ANGLE = 92
EYE_DEFAULT_STEP = 10


kit.servo[0].angle = EYE_DEFAULT_ANGLE

kit.servo[14].angle = DRIVER_DEFAULT_ANGLE

current_angle = 25
while current_angle != 0:
    current_angle -= 1
    kit.servo[14].angle = current_angle
    time.sleep(0.01)
    
while current_angle != 50:
    current_angle += 1
    kit.servo[14].angle = current_angle
    time.sleep(0.01)
    
while current_angle != 0:
    current_angle -= 1
    kit.servo[14].angle = current_angle
    time.sleep(0.01)
    
while current_angle != 50:
    current_angle += 1
    kit.servo[14].angle = current_angle
    time.sleep(0.01)

while current_angle != 25:
    current_angle -= 1
    kit.servo[14].angle = current_angle
    time.sleep(0.01)
    
# kit.servo[14].angle = DRIVER_MIN_ANGLE  # Reset servo to 0 degrees
# time.sleep(1)  # Pause between tests

