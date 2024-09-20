# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and set servol as pin 11 as PWM
GPIO.setup(11,GPIO.OUT)
servol = GPIO.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse


print ("starting to rotate")
#start PWM running, but with value of 0 (pulse off)
servol.start(0)
print ("Waiting for 2 seconds")
time.sleep(2)

# Define variable duty
duty = 2

# Loop for duty values from 2 to 12 (0 to 180 degrees)
while duty <= 12:
    servol.ChangeDutyCycle(duty)
    time.sleep(1)
    duty = duty + 1
    
# Wait a couple of seconds
time.sleep(2)

# Turn back to 180 degrees
print ("Turning back to 180 degrees in 2 seconds")
servol.ChangeDutyCycle(7)
time.sleep(2)
