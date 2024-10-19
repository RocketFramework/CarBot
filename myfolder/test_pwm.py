import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Create the I2C bus interface
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Create a PCA9685 instance
pca = PCA9685(i2c_bus)
pca.frequency = 50  # Typical for servos or LEDs

# Test PWM signal on channel 0
channel = pca.channels[15]

# Set the PWM duty cycle
#channel.duty_cycle = 0x3FFF  # 50% duty cycle
channel.duty_cycle = 0x0000
pca.deinit()
pca.reset()
