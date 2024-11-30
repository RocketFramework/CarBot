import sys
import platform
from pathlib import Path
import math
# Add the full path of 'my_folder' to sys.path
# if platform.system() == "Windows":
#     sys.path.append(str(Path(r"C:\Users\user_\CarBot\car\classes")))
# else:
#     sys.path.append(str(Path("/home/pi/Desktop/CarBot/car/classes")))
MINIMUM_SPEED = 20
MID_SPEED = 50
MAX_SPEED = 100
REVERSE_SPEED = abs(MID_SPEED - MINIMUM_SPEED)

MINIMUM_GAP = 0.5
MID_GAP = 1
HIGH_GAP = 2

GEAR_SHIFTING_TIME = 0.1
GEAR_INCRECEMENT_VALUE = 1
REVERSE_SLEEP_TIME = 1

WHEEL_RADIUS = 0.05
MAX_RPM = 120

ONE_WHEEL_TURN_LENGTH = 2*math.pi*WHEEL_RADIUS
ONE_WHEEL_TURN_STEPS = 26
WEB_SOCKET_SERVER_IP = "192.168.1.100"
WEB_SOCKET_SERVER_PORT = 65432

