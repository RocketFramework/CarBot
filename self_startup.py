import time
from car.full_self_driving import FullSelfDriving
from car.car_config import MINIMUM_GAP

auto_driver = FullSelfDriving()
time.sleep(7)

try:
    auto_driver.drive(MINIMUM_GAP)
except KeyboardInterrupt:
    auto_driver.stop_loop()
    auto_driver.cleanup()
    auto_driver = None
