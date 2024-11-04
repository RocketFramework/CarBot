import socket
import traceback
import threading
from car.full_self_driving import FullSelfDriving

driver = FullSelfDriving()

def send_error_to_server(client_socket, error_message):
    try:
        client_socket.sendall(f"error:{error_message}".encode())
    except Exception as e:
        print(f"Failed to send error to server: {e}")

def drive_with_error_handling(client_socket):
    try:
        driver.drive()
    except Exception as e:
        error = traceback.format_exc()
        print("An error occurred:", error)
        send_error_to_server(client_socket, f"Drive error: {error}")

def control_robot(client_socket, command):

    if command == "start":
        print("System startup initiated. Please standby...")
        car_thread = threading.Thread(target=drive_with_error_handling, args=(client_socket,))
        car_thread.start()
    elif command == "stop":
        print("Initiating stop sequence. Please standby...")
        driver.stop_loop()
    else:
        print("System shutting down. Please standby...")


def start_client(server_ip='127.0.0.1', server_port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server {server_ip}:{server_port}")

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data == "exit":
                print("Exiting...")
                driver.cleanup()
                break

            # Control the robot based on the command
            control_robot(client_socket, data)

    except Exception as e:
        print(e)
        send_error_to_server(client_socket, str(e.stack(context=1)))

    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    start_client()
