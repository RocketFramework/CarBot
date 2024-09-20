#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

in21 = 26
in22 = 19
in23 = 13
in24 = 6

in11 = 21
in12 = 20
in13 = 16
in14 = 12

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002

step_count = 8192 # 5.625*(1/64) per step, 4096 steps is 360°

direction1 = False # True for clockwise, False for counter-clockwise
direction2 = True 
# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in21, GPIO.OUT )
GPIO.setup( in22, GPIO.OUT )
GPIO.setup( in23, GPIO.OUT )
GPIO.setup( in24, GPIO.OUT )

GPIO.setup( in11, GPIO.OUT )
GPIO.setup( in12, GPIO.OUT )
GPIO.setup( in13, GPIO.OUT )
GPIO.setup( in14, GPIO.OUT )

# initializing
GPIO.output( in21, GPIO.LOW )
GPIO.output( in22, GPIO.LOW )
GPIO.output( in23, GPIO.LOW )
GPIO.output( in24, GPIO.LOW )

GPIO.output( in11, GPIO.LOW )
GPIO.output( in12, GPIO.LOW )
GPIO.output( in13, GPIO.LOW )
GPIO.output( in14, GPIO.LOW )

motor1_pins = [in11,in12,in13,in14]
motor2_pins = [in21,in22,in23,in24]
motor1_step_counter = 0 
motor2_step_counter = 7 

def cleanup():
    GPIO.output( in21, GPIO.LOW )
    GPIO.output( in22, GPIO.LOW )
    GPIO.output( in23, GPIO.LOW )
    GPIO.output( in24, GPIO.LOW )
    GPIO.output( in11, GPIO.LOW )
    GPIO.output( in12, GPIO.LOW )
    GPIO.output( in13, GPIO.LOW )
    GPIO.output( in14, GPIO.LOW )
    GPIO.cleanup()

# the meat
try:
    i = 0
    for i in range(step_count):
        for pin in range(0, len(motor1_pins)):
            GPIO.output( motor1_pins[pin], step_sequence[motor1_step_counter][pin] )
            GPIO.output( motor2_pins[pin], step_sequence[motor2_step_counter][pin] )
        if direction1==False:
            motor1_step_counter = (motor1_step_counter - 1) % 8
        elif direction1==True:
            motor1_step_counter = (motor1_step_counter + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
            
        if direction2==False:
            motor2_step_counter = (motor2_step_counter - 1) % 8
        elif direction2==True:
            motor2_step_counter = (motor2_step_counter + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( step_sleep )

except KeyboardInterrupt:
    cleanup()
    exit( 1 )

cleanup()
exit( 0 )