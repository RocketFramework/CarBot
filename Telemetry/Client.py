import socket
import traceback
import threading
from LOG.Logger import Logger
from FSD.Full_Self_Driving import FullSelfDriving

from Car.config import ERROR_LOG_FILE_PATH, INFO_LOG_FILE_PATH

log = Logger()
open(INFO_LOG_FILE_PATH, 'w').close()
open(ERROR_LOG_FILE_PATH, 'w').close()

last_position = 0 

def send_log_to_server(client_socket, log_file_path):
    global last_position
    try:
        with open(log_file_path, "r") as log_file:
            log_file.seek(last_position)  # Move to last read position
            for line in log_file:
                client_socket.sendall(line.encode())
            last_position = log_file.tell()  # Update position
    except Exception as e:
        print(f"Error: Failed to send log to server: {e}")

def send_error_to_server(client_socket, error_message):
    try:
        client_socket.sendall(f"Error:{error_message}".encode())
    except Exception as e:
        print(f"Error: Failed to send error to server: {e}")
        log.log(type="error", message="Failed to send error to server")

def drive_with_error_handling(client_socket, auto_driver):
    try:
        auto_driver.drive()
    except Exception as e:
        error = traceback.format_exc()
        print("An error occurred:", error)
        send_error_to_server(client_socket, f"Error: Auto-Driving: {error}")
        log.log(type="error", message="FULL SELF DRIVING ERROR")

def control_robot(client_socket, command, auto_driver=None):

    if command == "start":
        if auto_driver:
            auto_driver.stop_loop()
            auto_driver = None

        if not auto_driver:
            auto_driver = FullSelfDriving()
            print("Auto Drive: Starting autonomous driving mode...")
            car_thread = threading.Thread(target=drive_with_error_handling, args=(
                client_socket, auto_driver,))
            car_thread.start()

    elif command == "stop":
        if auto_driver:
            print("Auto Drive: Stopping autonomous driving mode...")
            auto_driver.stop()
            auto_driver = None

    elif command == "exit":
        if auto_driver:
            auto_driver.stop()

    return auto_driver

def connect_to_server(server_ip='127.0.0.1', server_port=65432):
    # Create and Configure the Client Socket
    """Connect to the server and handle communication."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server {server_ip}:{server_port}")

    auto_driver = None
    exit_event = threading.Event()

    def receive_and_control():
        """Handle incoming commands and control the robot."""
        nonlocal auto_driver
        
        while not exit_event.is_set():
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                if data == "exit":
                    print("Exiting...")
                    exit_event.set()
                    if auto_driver:
                        auto_driver.stop()
                    break

                auto_driver = control_robot(
                    client_socket, data, auto_driver)

            except Exception as e:
                print(f"Error receiving command: {e}")
                exit_event.set()
                break

    def log_sender():
        """Continuously send logs to the server."""
        while not exit_event.is_set():
            try:
                send_log_to_server(client_socket, INFO_LOG_FILE_PATH)
                threading.Event().wait(2)  # wait for 2 seconds before sending next log
            except Exception as e:
                print(f"Error sending log: {e}")
                break

    # Start threads
    command_thread = threading.Thread(target=receive_and_control, daemon=True)
    log_thread = threading.Thread(target=log_sender, daemon=True)

    command_thread.start()
    log_thread.start()

    command_thread.join()
    threading.Event().wait(0.5)  # give log thread time to shut down
    client_socket.close()

def intelligent_start_system(server_ip='127.0.0.1', server_port=65432):
    """Initialize the system and connect to the server."""
    try:
        connect_to_server(server_ip, server_port)
    except ConnectionRefusedError:
        print("Failed to connect to server")
        log.log(type="error", message="Connection Refused Error")

if __name__ == "__main__":
    intelligent_start_system()