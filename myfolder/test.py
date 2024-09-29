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
    
    set_servo_position(0, 0)   
    print("moved to 0")
    time.sleep(5)      
    set_servo_position(0, 30)   
    print("moved to 30")
    time.sleep(5)      
    set_servo_position(0, 60) 
    print("moved to 60")  
    time.sleep(5)      
    set_servo_position(0, 90)   
    print("moved to 90")
    time.sleep(5)      
    set_servo_position(0, 120)   
    print("moved to 120")  
    time.sleep(5)      
    set_servo_position(0, 150)   
    print("moved to 150")  
    time.sleep(5)               
    set_servo_position(0, 180)   
    print("moved to 180")  
    time.sleep(5)      
    set_servo_position(0, 210)   
    print("moved to 210")  
    time.sleep(5)      
    set_servo_position(0, 240)   
    print("moved to 240")  
    time.sleep(5)      
    set_servo_position(0, 270)   
    print("moved to 270")  
    time.sleep(5)      
    set_servo_position(0, 300)   
    print("moved to 300")  
    time.sleep(5)      
    set_servo_position(0, 330)   
    time.sleep(5)  
    print("moved to 330") 
# 90
# 150
# 180
# 210
# 240
# 270
# 300

except KeyboardInterrupt:
    pca.channels[0].duty_cycle = 0  # Turn off Servo 0
    pca.channels[1].duty_cycle = 0  # Turn off Servo 1
