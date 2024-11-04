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
TURN_STEP_SIZE = 1

EYE_MAX_ANGLE = 115
EYE_MIN_ANGLE = 65
EYE_ACTUATION_RANGE = 150 # This must be adjusted
EYE_DEFAULT_ANGLE = 90
EYE_DEFAULT_STEP = 10


#67
#117

kit.servo[14].angle = 25.5
time.sleep(2)
kit.servo[0].angle = 92


# kit.servo[14].angle = DRIVER_MIN_ANGLE  # Reset servo to 0 degrees
# time.sleep(1)  # Pause between tests

