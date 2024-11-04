import socket

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
            command = input("Enter command (start/stop/exit): ").strip().lower()

            if command in ["start", "stop", "exit"]:
                conn.sendall(command.encode())
                
                if command == "exit":
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
                print("Invalid command. Use 'start', 'stop', or 'exit'.")

    finally:
        conn.close()
        server_socket.close()
        print("Connection closed")
