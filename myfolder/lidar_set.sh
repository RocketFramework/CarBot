# This should Be Run on every Debug
# Serial Port Conflicts
# /dev/serial0 might be shared with the Pi console or Bluetooth if not properly configured.

# Fix:

# Ensure UART is enabled and login shell over serial is disabled.

# Run sudo raspi-config → Interface Options → Serial → Disable login shell, enable serial hardware.
sudo usermod -a -G dialout pi
sudo chmod 666 /dev/serial0
groups
