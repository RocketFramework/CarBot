from pymavlink import mavutil
import time

# Connect to Pixhawk
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600)
master.wait_heartbeat()
print("Connected to Pixhawk")

def set_servo(channel, pwm):
    """
    channel: servo output number (1–16)
    pwm: PWM value in microseconds (1000–2000)
    """
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,
        channel,
        pwm,
        0, 0, 0, 0, 0
    )

# Example: Move servo on channel 1
set_servo(1, 1500)   # center
time.sleep(1)
set_servo(1, 1800)   # one extreme
time.sleep(1)
set_servo(1, 1200)   # other extreme
time.sleep(1)
set_servo(1, 1500)   # back to center
