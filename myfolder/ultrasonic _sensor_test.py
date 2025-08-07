import RPi.GPIO as GPIO
import time

def measure_distance():
    GPIO.setmode(GPIO.BOARD)
    PIN_TRIGGER = 7
    PIN_ECHO = 11

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    time.sleep(2)

    # Send trigger pulse
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    # Wait for echo start with timeout
    timeout_start = time.time()
    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
        if pulse_start_time - timeout_start > 0.01:
            print("Timeout: Echo start not received")
            return None

    # Wait for echo end with timeout
    timeout_start = time.time()
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()
        if pulse_end_time - timeout_start > 0.01:
            print("Timeout: Echo end not received")
            return None

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    return distance

try:
    while True:
        dist = measure_distance()
        if dist is not None:
            print(f"Distance: {dist} cm")
finally:
    GPIO.cleanup()

