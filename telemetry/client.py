import socket
import traceback
import threading
from car.full_self_driving import FullSelfDriving
from car.full_manual_driving import FullManualDriving
from car.car_config import MINIMUM_GAP

MINIMUM_GAP = MINIMUM_GAP

def send_error_to_server(client_socket, error_message):
    try:
        client_socket.sendall(f"Error:{error_message}".encode())
    except Exception as e:
        print(f"Error:Failed to send error to server: {e}")

def drive_with_error_handling(client_socket, auto_driver, MINIMUM_GAP):
    try:
        auto_driver.drive(MINIMUM_GAP)
    except Exception as e:
        error = traceback.format_exc()
        print("An error occurred:", error)
        send_error_to_server(client_socket, f"Error:Auto-Driving: {error}")

def control_robot(client_socket, command, auto_driver=None, manual_driver=None):
    global MINIMUM_GAP
    
    if command in ["1","2","3","4","5"]:
        MINIMUM_GAP = command
        
    if command == "start":
        if auto_driver:
            auto_driver.stop_loop()
            auto_driver = None

        if not auto_driver:
            auto_driver = FullSelfDriving()
            print("Auto Drive: Starting autonomous driving mode...")
            car_thread = threading.Thread(target=drive_with_error_handling, args=(client_socket, auto_driver, MINIMUM_GAP,))
            car_thread.start()

    elif command == "stop":
        if auto_driver:
            print("Auto Drive: Stopping autonomous driving mode...")
            auto_driver.stop_loop()
            auto_driver = None

    elif command == "m":
        if auto_driver:
            print("Auto Drive: Switching to manual driving mode...")
            auto_driver.stop_loop()
            auto_driver.cleanup()
            auto_driver = None

        if not manual_driver:
            manual_driver = FullManualDriving()
            print("Manual Drive: Switching to manual mode...")

    if command == "f":
        if not manual_driver:
            manual_driver = FullManualDriving()
            print("Manual Drive: Switching to manual mode...")
            
        if manual_driver:
            print("Manual Drive: Moving forward...")
            manual_driver.drive("Front")
        
    elif command == "b":
        if not manual_driver:
            manual_driver = FullManualDriving()
            print("Manual Drive: Switching to manual mode...")
            
        if manual_driver:
            print("Manual Drive: Moving backward...")
            manual_driver.drive("Back")

    elif command == "r":
        if not manual_driver:
            manual_driver = FullManualDriving()
            print("Manual Drive: Switching to manual mode...")
            
        if manual_driver:
            print("Manual Drive: Turning right...")
            manual_driver.drive("Right")

    elif command == "l":
        if not manual_driver:
            manual_driver = FullManualDriving()
            print("Manual Drive: Switching to manual mode...")
            
        if manual_driver:
            print("Manual Drive: Turning left...")
            manual_driver.drive("Left")

    elif command == "a":
        if manual_driver:
            print("Manual Drive: Switching to auto drive mode...")
            
            manual_driver.stop()
            manual_driver.cleanup()
            manual_driver = None

    elif command == "s":
        if not manual_driver:
            manual_driver = FullManualDriving()
            print("Manual Drive: Switching to manual mode...")
            
        if manual_driver:
            print("Manual Drive: Stopping vehicle...")
            manual_driver.stop()

    return auto_driver, manual_driver

def start_client(server_ip='127.0.0.1', server_port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server {server_ip}:{server_port}")

    auto_driver = None
    manual_driver = None

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data == "exit":
                print("Exiting...")
                if auto_driver:
                    auto_driver.cleanup()
                if manual_driver:
                    manual_driver.cleanup()
                break

            # Control the robot based on the command
            auto_driver, manual_driver = control_robot(client_socket, data, auto_driver, manual_driver)

    except Exception as e:
        e = traceback.format_exc()
        print(f"Error{e}")
        send_error_to_server(client_socket, e)

    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    start_client()
