import re
import socket
import threading
import traceback
from datetime import datetime
from Car.config import SERVER_LOG

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
            command = get_user_input()
            if command in ["start", "stop", "exit"]:
                conn.sendall(command.encode())

                if command == "exit":
                    conn.sendall(command.encode())
                    stop_event.set()
                    break

            else:
                print("Error: Invalid command. Use 'start', 'stop' or 'exit'.\n")


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