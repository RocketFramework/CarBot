import socket

def start_server(host='127.0.0.1', port=65432):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
    # Bind the socket to the address and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    # Accept a connection
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    try:
        while True:
            # Send commands to the client
            command = input("Enter command (start/stop/exit): ").strip().lower()

            if command in ["start", "stop"]:
                conn.sendall(command.encode())
            elif command == "exit":
                conn.sendall(command.encode())
                break
            else:
                print("Invalid command. Use 'start', 'stop', or 'exit'.")

    finally:
        # Close the connection
        conn.close()
        server_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    start_server()
