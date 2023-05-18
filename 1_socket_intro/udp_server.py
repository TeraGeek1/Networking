# UDP Server side
import socket

# Create a server side socket IPv4 (AF_INET) and UDP (SOCK_DGRAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to tuple (IP addr, port num)
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))

# We are not listening or accepting connections since UDP is connectionless protocol

message, address = server_socket.recvfrom(1024)

print(message.decode("utf-8"))
print(address)
