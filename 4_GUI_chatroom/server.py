# GUI chat room Server side
import socket as soc
import threading

## Def const vars
HOST_IP = soc.gethostbyname(soc.gethostname())
HOST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

## Server socket
server_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
server_soc.bind((HOST_IP, HOST_PORT))
server_soc.listen()

## Create two blank list to store connected client sockets and names
client_soc_list = []
client_name_list = []


def broadcast_message(message: bytes or str):
    """Send a message to ALL clients"""

    for client_socket in client_soc_list:
        client_socket.send(message)


def receive_message(client_socket: soc.socket):
    """Receive an incoming message from a specific client and forward the message to be broadcast"""

    while True:
        try:
            ## Get the name of the given client
            index = client_soc_list.index(client_socket)
            name = client_name_list[index]

            ## Receive a message from the client socket
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            message = f"{name}: {message}"
            broadcast_message(message.encode(ENCODER))

        except:
            ## Find the index of the client socket in our list
            index = client_soc_list.index(client_socket)
            name = client_name_list[index]

            ## Remove the client socket and the name from the lists
            client_soc_list.remove(client_socket)
            client_name_list.remove(name)

            ## Close the client socket
            client_socket.close()

            ## Broadcast the the client has left the chat
            broadcast_message(f"{name} has left the chat".encode(ENCODER))
            break


def connect_client():
    """Connect a incoming client to the server"""

    while True:
        ## Accept any incoming client connections
        client_soc, client_addr = server_soc.accept()
        print(f"Connected with {client_addr}...")

        ## Send a NAME flag to prompt the client for their name
        client_soc.send("@_NAME".encode(ENCODER))
        client_name = client_soc.recv(BYTESIZE).decode(ENCODER)

        ## Add new client socket and client name to appropriate lists
        client_soc_list.append(client_soc)
        client_name_list.append(client_name)

        ## Update the server, individual client, and ALL clients
        print(f"Name of new client: {client_name}\n")  # Server
        client_soc.send(
            f"{client_name}, you have connected to the server!".encode(ENCODER)
        )  # individual client
        broadcast_message(f"{client_name} has joined the chat!".encode(ENCODER))

        ## Now that a new client has connected, start a thread
        receive_thread = threading.Thread(target=receive_message, args=(client_soc,))
        receive_thread.start()


## Start the server
print("\nNow listen for incoming connections...\n")
connect_client()
