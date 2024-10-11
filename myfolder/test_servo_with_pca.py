import time
from adafruit_servokit import ServoKit

# Initialize the PCA9685 board (16 channels)
kit = ServoKit(channels=16)

# Test each channel to see if a motor/servo is connected
for channel in range(16):
    print(f"Testing motor/servo on channel {channel}")
    kit.servo[channel].angle = 30  # Set servo to 90 degrees
    time.sleep(2)  # Wait for the motor/servo to move
    kit.servo[channel].angle = 51  # Reset servo to 0 degrees
    time.sleep(1)  # Pause between tests

