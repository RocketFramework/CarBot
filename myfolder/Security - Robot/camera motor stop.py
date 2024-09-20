import cv2
import RPi.GPIO as GPIO
import time

# Set up GPIO for the stepper motor
GPIO.setmode(GPIO.BCM)
# Define your motor pins
motor_pins = [26, 19, 13, 6]  # Adjust these pins based on your stepper motor wiring 
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Set up the camera
camera = cv2.VideoCapture(0)  # Use 0 for the default camera

# Function to stop the stepper motor
def stop_motor():
    for pin in motor_pins:
        GPIO.output(pin, 0)

# Main loop
try:
    _, prev_frame = camera.read()

    while True:
        _, frame = camera.read()

        # Convert frames to grayscale for simplicity
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate absolute difference between frames
        frame_diff = cv2.absdiff(prev_gray, gray)

        # Set a threshold for change detection
        threshold = 30
        _, threshold_diff = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)

        # Count non-zero pixels in the thresholded difference
        non_zero_count = cv2.countNonZero(threshold_diff)

        if non_zero_count > 0:
            # Movement detected, do something (you can move the motor here)
            print("Movement detected!")
            
        else:
            # No movement, stop the motor
            stop_motor()
            print("No movement detected.")

        # Update the previous frame
        prev_frame = frame

except KeyboardInterrupt:
    # Clean up GPIO on program exit
    GPIO.cleanup()
    camera.release()