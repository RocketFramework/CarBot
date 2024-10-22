import socket
import sys
import os
import threading
from pathlib import Path

from car.full_self_driving import FullSelfDriving

driver = FullSelfDriving()
def control_robot(command):
    if command == "start":
        print("Robot car starting...")
        # Add code to start the motors, etc.
        car_thread = threading.Thread(target=driver.drive)
        car_thread.start()
    elif command == "stop":
        print("Robot car stoppingrrr...")
        # Add code to stop the motors
        driver.stop_loop()
    else:
        print("Unknown command received.")

def start_client(server_ip='127.0.0.1', server_port=65432):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the server's address
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server {server_ip}:{server_port}")

    try:
        while True:
            # Receive the command from the server
            data = client_socket.recv(1024).decode()

            if not data:
                break

            if data == "exit":
                print("Exiting...") 
                driver.cleanup()
                break

            # Control the robot based on the command
            control_robot(data)
            
    finally:
        # Close the connection
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    start_client()
