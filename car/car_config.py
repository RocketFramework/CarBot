import sys
import platform
from pathlib import Path
import math
# Add the full path of 'my_folder' to sys.path
# if platform.system() == "Windows":
#     sys.path.append(str(Path(r"C:\Users\user_\CarBot\car\classes")))
# else:
#     sys.path.append(str(Path("/home/pi/Desktop/CarBot/car/classes")))
MINIMUM_SPEED = 30
MID_SPEED = 60
MAX_SPEED = 100
REVERSE_SPEED = abs(MID_SPEED - MINIMUM_SPEED)

MINIMUM_GAP = 0.8
MID_GAP = 1.2
HIGH_GAP = 2

GEAR_SHIFTING_TIME = 0.1
GEAR_INCRECEMENT_VALUE = 1
REVERSE_SLEEP_TIME = 1

WHEEL_RADIUS = 0.05
MAX_RPM = 120

ONE_WHEEL_TURN_LENGTH = 2*math.pi*WHEEL_RADIUS
ONE_WHEEL_TURN_STEPS = 26
WEB_SOCKET_SERVER_IP = "192.168.1.6"
WEB_SOCKET_SERVER_PORT = 65432



if platform.system() == "Windows":
    INFO_LOG_FILE_PATH = r'C:\Users\user_\CarBot\client_log.log'
    ERROR_LOG_FILE_PATH = r'C:\Users\user_\CarBot\cronlogfile.log'
    SERVER_LOG = r'C:\Users\user_\CarBot\server_log.log'
else:
    INFO_LOG_FILE_PATH = '/home/pi/Documents/CarBot/client_log.log'
    ERROR_LOG_FILE_PATH = '/home/pi/Documents/CarBot/cronlogfile.log'
    SERVER_LOG = '/home/pi/Documents/CarBot/carbot.log'