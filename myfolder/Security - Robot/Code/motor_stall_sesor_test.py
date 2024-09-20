import RPi.GPIO as GPIO
import time
#26, 19, 13, 6
DIR = 26# Direction pin
STEP = 19# Step pin
STALL_PIN = 13# GPIO pin connected to a stall detection switch (simulated)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(STALL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.output(STEP, GPIO.LOW)
GPIO.setup(DIR, GPIO.LOW)
# Function to move the stepper motor with stall detection
def move_stepper_with_stall_detection(steps, direction):
    GPIO.output(DIR, direction)
    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(0.05)# Adjust delay based on your motor's specifications       
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(0.05)

        # Check stall detection switch       
        if GPIO.input(STALL_PIN) == GPIO.LOW:
            print("Stall detected. Possible barrier.")
            break

# Move the stepper motor with stall detection
move_stepper_with_stall_detection(100, GPIO.HIGH)# Adjust the number of steps and direction
# Clean up GPIO
GPIO.cleanup()