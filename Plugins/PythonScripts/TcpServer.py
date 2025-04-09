import socket
import struct
# import numpy as np

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 12345      # Port to listen on

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an IP and port
server_socket.bind((HOST, PORT))

# Start listening for connections
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}...")

while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print(f"Connected by {client_address}")

    try:
        while True:
            # Receive data from the client
            '''
            data = client_socket.recv(312)
            if not data:
                break
            print(f"Received: {data}")
            floats = struct.unpack('<78f', data)
            position = [floats[i:i+3] for i in range(0, len(floats), 3)]
            print("vector:", position)
            '''
            data = client_socket.recv(312) # Receive 312 bytes (26 × 3 × 4)
            floats = struct.unpack('<78f', data) # 78 little-endian floats

# Group into 3D vectors
            position_vectors = [floats[i:i+3] for i in range(0, len(floats), 3)]

# Now position_vectors is a list of [x, y, z] lists
            print(position_vectors)
            # Send a response back
            response = "Hello from Python!"
            client_socket.sendall(response.encode('utf-8'))
    except ConnectionResetError:
        print("Connection lost.")
    finally:
        # Close the connection with the client
        client_socket.close()
        print(f"Disconnected from {client_address}")
