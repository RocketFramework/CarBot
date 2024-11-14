import socket
import traceback
from car.car_config import MID_GAP

def start_server(host='127.0.0.1', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    try:

        while True:
            mode = input(
                "--Select Driving Mode--\n"
                "Auto-Drive :1\n" 
                "Manual     :2\n" 
                "Exit       :3\n"
                "Enter Drive-Mode: ")
            print()
            
            if mode == "1":
                mode = 1
                break

            elif mode == "2":
                mode = 2
                break

            elif mode == "3":
                mode = 3
                break

            else:
                print("Error: Invalid Command")
                continue
        while True:
            if mode == 1:
                try:
                    command = float(input("Enter the Minimum Gap of Obstacle in Meters: "))
                    if 0 < command < MID_GAP:
                        command = str(command)
                        conn.sendall(command.encode())
                        break
                    else:
                        print(f"Error: Please enter a gap between 0 and {MID_GAP} meters.")
                        continue
                except ValueError:
                    print("Error: Invalid gap value. Please enter a valid number.")
                    continue
            else:
                break
        while True:
            if mode == 1:
                command = input(
                    "Start\n" 
                    "Stop\n" 
                    "Switch-Mode:M\n" 
                    "Exit\n" 
                    "Enter command: ").strip().lower()
                print()
                
                if command in ["start", "stop", "m", "exit"]:
                    
                    conn.sendall(command.encode())
                    
                    if command  == "stop":
                        while True:
                            try :
                                command = float(input("Enter the Minimum Gap of Obstacle in Meters : "))
                                print()
                                if 0 < command < MID_GAP:
                                    command = str(command)
                                    conn.sendall(command.encode())
                                    break
                                else:
                                    print(f"Error:Please enter a gap between 0 and {MID_GAP} meters\n")
                                    continue
                            except Exception:
                                e = traceback.format_exc()
                                print(e)
                                
                    if command == "m":
                        mode = 2

                    if command == "exit":
                        conn.sendall(command.encode())
                        break

                    # Wait briefly to check for errors
                    conn.settimeout(1)
                    try:
                        data = conn.recv(1024).decode()
                        if data.startswith("error:"):
                            print(f"Client: {data[6:]}")
                    except socket.timeout:
                        # No error received within the timeout period
                        continue
                else:
                    print("Error:Invalid command. Use 'start', 'stop', or 'exit'.\n")
            if mode == 2:
                command = input(
                                "Move Forward   :F\n"
                                "Move Backward  :B\n"
                                "Turn Right     :R\n"
                                "Turn Left      :L\n"
                                "Stop           :S\n"
                                "Switch-Mode    :A\n"
                                "Exit           :X\n"
                                "Enter command: "
                            ).strip().lower()
                print()
                    
                if command in ["f", "b", "r", "s", "l", "a", "x"]:
                    conn.sendall(command.encode())

                    if command == "a":
                        mode = 1

                    if command == "x":
                        mode = 3
                        new_command = "exit"
                        conn.sendall(new_command.encode())
                        break

                    # Wait briefly to check for errors
                    conn.settimeout(1)
                    try:
                        data = conn.recv(1024).decode()
                        if data.startswith("error:"):
                            print(f"Error: {data[6:]}")
                    except socket.timeout:
                        # No error received within the timeout period
                        continue
                else:
                    print("Error:Invalid command. Use 'f', 'b', 'r',  'l', 'a' or 'x'.\n")
                    
            if mode == 3:
                command = "exit"
                conn.sendall(command.encode())
                break
    finally:
        conn.close()
        server_socket.close()
        print("System Shuting-Down -> Engine off")
