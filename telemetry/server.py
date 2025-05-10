import re
import socket
import threading
import traceback
from datetime import datetime
from car.car_config import MID_GAP, MINIMUM_GAP, SERVER_LOG

LOG_FILE_PATH = SERVER_LOG
open(LOG_FILE_PATH, 'w').close()

def listen_for_logs(conn, stop_event):                         
    while not stop_event.is_set():
        try:
            conn.settimeout(1.0)
            data = conn.recv(1024).decode().strip()
            if data:
                with open(LOG_FILE_PATH, "a") as log_file:
                    log_file.write(data + "\n")
        except socket.timeout:
            continue
        except Exception:
            break

def get_user_input():
    command = input(
        "Start\n" 
        "Stop\n" 
        "Settings:S\n" 
        "Exit\n" 
        "Enter command: ").strip().lower()
    print()
    return command

def start_server(host='127.0.0.1', port=65432):
    # Create and Configure the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    stop_event = threading.Event()
    
    log_thread = threading.Thread(target=listen_for_logs, args=(conn, stop_event))
    log_thread.start()

    try:
        while True:
            mode = input(
                "--Select Driving Mode--\n"
                "Auto-Drive :1\n" 
                "Manual     :2\n" 
                "Exit       :3\n"
                "Enter Drive-Mode: ").strip()
            print()
            
            if mode in ["1", "2", "3"]:
                mode = int(mode)
                break
            else:
                print("Error: Invalid Command")
        
        while True:
            if mode == 1:
                command = get_user_input()
                if command in ["start", "stop", "s", "exit"]:
                    conn.sendall(command.encode())

                    if command == "s":
                        while True:
                            try:
                                val = input("Enter the Minimum Gap of Obstacle in Meters: ").strip()
                                if val == '':
                                    conn.sendall(str(MINIMUM_GAP).encode())
                                    break
                                elif any(c.isalpha() for c in val) or re.search(r'\.{2,}', val):
                                    print(f"Error: Please enter a gap between 0 and {MID_GAP} meters. (Use numbers)")
                                else:
                                    val = float(val)
                                    if 0 < val < MID_GAP:
                                        conn.sendall(str(val).encode())
                                        break
                                    else:
                                        print(f"Error: Please enter a gap between 0 and {MID_GAP} meters.")
                            except Exception:
                                print(traceback.format_exc())

                    if command == "exit":
                        conn.sendall(command.encode())
                        stop_event.set()
                        break

                else:
                    print("Error: Invalid command. Use 'start', 'stop', 's' or 'exit'.\n")

            elif mode == 2:
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
                        conn.sendall("exit".encode())
                        stop_event.set()
                        break

                else:
                    print("Error:Invalid command. Use 'f', 'b', 'r',  'l', 'a' or 'x'.\n")

            elif mode == 3:
                conn.sendall("exit".encode())
                stop_event.set()
                break

    finally:
        stop_event.set()  
        try:
            conn.shutdown(socket.SHUT_RDWR)  
        except Exception:
            pass 
        conn.close()  
        log_thread.join() 
        server_socket.close()
        print("System Shutting Down -> Engine Off")

