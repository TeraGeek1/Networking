# TCP Server Side

import socket

# Create a server side socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# See how to get IP address dynamically
print(socket.gethostname())  # My Host name
print(socket.gethostbyname(socket.gethostname()))  # IP of given host // this pc's IPv4 Address

# Bind our new socket to a tuple (IP ADDRESS, Port Address)
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))

# put the socket into listening mode to listen for any possible connections
server_socket.listen()

# Listen forever to accept ANY connection
while True:
    # Accept every single connection and store twp pieces of info
    client_socket, client_address = server_socket.accept()
    # print(type(client_socket))
    # print(client_socket)

    # print(type(client_address))
    # print(client_address)

    print(f"Connected to {client_address}! \n")

    # Send a message to The client
    client_socket.send(f"You are connected to {socket.gethostbyname(socket.gethostname())}".encode("utf-8"))

    # Close the server socket
    server_socket.close()
    break
