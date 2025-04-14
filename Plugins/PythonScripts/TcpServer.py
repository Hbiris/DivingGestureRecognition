import socket
import struct
import random
import numpy as np

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 12345      # Port to listen on
GESTURE_HOST = '127.0.0.1'
GESTURE_PORT = 5005

# Hand_joint coordinate list for 26 joints. See hand_coordinate.pdf
# index_list = [1,2,3,4,5,7,8,9,10,12,13,14,15,17,18,19,20,22,23,24,25]

# If above index list is wrong, try the one below
index_list = [0,1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19,21,22,23,24]

# Create socket objects
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# gesture_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an IP and port (receive data)
server_socket.bind((HOST, PORT))

# Connect the socket to an IP and port (send data)
# gesture_server_socket.connect((GESTURE_HOST, GESTURE_PORT))

# Start listening for connections
server_socket.listen(5)
# print(f"Server listening on {HOST}:{PORT}...")

while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    # print(f"Connected by {client_address}")

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
            data = client_socket.recv(312) # Receive 312 bytes (26 × 3 × 4
            

            floats = struct.unpack('<78f', data) # 78 little-endian floats


            # Group into 3D vectors
            position_vectors = [floats[i:i+3] for i in range(0, len(floats), 3)]

            # Now position_vectors is a list of [x, y, z] lists
            print(position_vectors)

            # Select the correspoding index and Flatten to 1d vectors
            flat_list = [coord for idx in index_list for coord in position_vectors[idx]]
            
            if len(flat_list) != 63:
                raise ValueError("flat_list length is not 63.")
            
            # Send a response back
            response = "Hello from Python!"
            client_socket.sendall(response.encode('utf-8'))

            # Send response to gesture model
            arr = np.array(flat_list, dtype=np.float32)
            # gesture_server_socket.sendall(arr.tobytes())
    
    except ConnectionResetError:
        print("Connection lost.")
    
    finally:
        # Close the connection with the client
        client_socket.close()
        server_socket.close()
        # gesture_server_socket.close()
        # print(f"Disconnected from all 3 sockets")