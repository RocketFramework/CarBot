import time
from adafruit_pca9685 import PCA9685
import board
import busio

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Typical frequency for servos

# Function to set the servo position
def set_servo_position(channel, angle):
    pulse = int((angle / 180.0 * 2000) + 500)  # Convert angle to pulse length
    pca.channels[channel].duty_cycle = pulse

# Example: Move both servos to different angles
try:
    while True:
        set_servo_position(0, 0)    # Move Servo 0 to 0 degrees
        set_servo_position(1, 90)   # Move Servo 1 to 90 degrees
        time.sleep(1)               # Wait 1 second

        set_servo_position(0, 90)   # Move Servo 0 to 90 degrees
        set_servo_position(1, 180)  # Move Servo 1 to 180 degrees
        time.sleep(1)               # Wait 1 second

        set_servo_position(0, 180)  # Move Servo 0 to 180 degrees
        set_servo_position(1, 0)    # Move Servo 1 to 0 degrees
        time.sleep(1)               # Wait 1 second

except KeyboardInterrupt:
    pca.channels[0].duty_cycle = 0  # Turn off Servo 0
    pca.channels[1].duty_cycle = 0  # Turn off Servo 1
