import logging
import threading
import time
import RPi.GPIO as GPIO
import time
import dlib
from camera_movement_controller import HumanTracker

# from motor_movement import move_vertically as move_vertically
# move_vertically("right")

# from motor_movement import move_horizontally as move_horizontally
# move_horizontally("right") #movable
#
humanTracker = HumanTracker()
humanTracker.start_tracking()

exit( 0 )
