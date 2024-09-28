import threading
import time
import logging
import signal
import sys
from logging.handlers import RotatingFileHandler
from car.telemetry import Telemetry
from car.websocket.client import send_telemetry
from car.auto_pilot import Auto_Pilot
from car.utils.logger_config import setup_logger

# Set up logger
logger = setup_logger("main", log_file='carbot.log')

running = True

def signal_handler(sig, frame):
    global running
    logger.info("Shutdown signal received. Stopping CARBOT.")
    running = False

signal.signal(signal.SIGINT, signal_handler)

def auto_run_car(car):
    while running:
        car.drive()
        logger.info("Car is driving...")
        time.sleep(0.1)
    logger.info("Car auto-driving stopped.")

def send_telemetry_data(telemetry):
    while running:
        data = telemetry.gather_data()
        logger.info(f"Telemetry Data: {data}")
        send_telemetry(data)
        time.sleep(1)
    logger.info("Telemetry sending stopped.")

def main():
    telemetry = Telemetry()
    car = Auto_Pilot()

    logger.info("Starting CARBOT system...")

    car_thread = threading.Thread(target=auto_run_car, args=(car,))
    telemetry_thread = threading.Thread(target=send_telemetry_data, args=(telemetry,))

    car_thread.start()
    telemetry_thread.start()

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down CARBOT...")

    car_thread.join()
    telemetry_thread.join()

    logger.info("CARBOT system shut down gracefully.")
    
if __name__ == "__main__":
    main()
