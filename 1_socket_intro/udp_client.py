# UDP Client side
import socket

# Create a UDP IPv4 socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send some info via a connectionless protocol
client_socket.sendto("Hi server!!".encode("utf-8"), (socket.gethostbyname(socket.gethostname()), 12345))
