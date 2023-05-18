# TCP client side

import socket

# Create a client side IPv4 socket (AF_INET) and UTP (SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to a server located at a given IP and port
client_socket.connect((socket.gethostbyname(socket.gethostname()), 12345))
# client_socket.connect( ("10.0.0.151", 12345) )

# Receive a message from the server...You must specify the max number of bytes to receive
message = client_socket.recv(1024).decode("utf-8")
print(f"\n{message}\n")

# Close the client socket
client_socket.close()
