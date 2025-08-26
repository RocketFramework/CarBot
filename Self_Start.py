import time
from FSD.Full_Self_Driving import FullSelfDriving

auto_driver = FullSelfDriving()
time.sleep(1)

try:
    auto_driver.drive()
except KeyboardInterrupt:
    auto_driver.stop()
    auto_driver = None