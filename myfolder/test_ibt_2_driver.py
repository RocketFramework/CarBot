import RPi.GPIO as GPIO
import time

# Use Broadcom pin numbering
GPIO.setmode(GPIO.BCM)

# Define GPIO pins connected to BTS7960
RPWM_PIN = 18  # GPIO18 (Pin 12)
LPWM_PIN = 19  # GPIO19 (Pin 35)
REN_PIN  = 23  # GPIO23 (Pin 16)
LEN_PIN  = 24  # GPIO24 (Pin 18)

# Set up GPIO pins as outputs
GPIO.setup(RPWM_PIN, GPIO.OUT)
GPIO.setup(LPWM_PIN, GPIO.OUT)
GPIO.setup(REN_PIN, GPIO.OUT)
GPIO.setup(LEN_PIN, GPIO.OUT)

# Initialize PWM on RPWM and LPWM
PWM_FREQ = 2500  # Frequency in Hz

rpwm = GPIO.PWM(RPWM_PIN, PWM_FREQ)
lpwm = GPIO.PWM(LPWM_PIN, PWM_FREQ)

rpwm.start(0)  # Start with 0% duty cycle
lpwm.start(0)

try:
    print("Moving Forward at 50% speed...")
    GPIO.output(REN_PIN, GPIO.HIGH)  # Enable Right
    GPIO.output(LEN_PIN, GPIO.HIGH)   # Disable Left
    rpwm.ChangeDutyCycle(100)          # 50% speed
    lpwm.ChangeDutyCycle(0)
    time.sleep(5)

    print("Moving Reverse at 50% speed...")
    GPIO.output(REN_PIN, GPIO.HIGH)    # Disable Right
    GPIO.output(LEN_PIN, GPIO.HIGH)   # Enable Left
    lpwm.ChangeDutyCycle(100)           # 50% speed
    rpwm.ChangeDutyCycle(0)
    time.sleep(5)

    print("Stopping Motor...")
    GPIO.output(REN_PIN, GPIO.LOW)
    GPIO.output(LEN_PIN, GPIO.LOW)
    rpwm.ChangeDutyCycle(0)
    lpwm.ChangeDutyCycle(0)
    time.sleep(2)

finally:
    rpwm.stop()
    lpwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup completed.")
