# Chat room client side
import socket as soc
import threading

## Def const vars
# DEST_IP = soc.gethostbyname(soc.gethostname()) # Local server
DEST_IP = "10.0.0.100"  # My Desktop pc
DEST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

## Create a client socket IPv4 and TCP
client_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
client_soc.connect((DEST_IP, DEST_PORT))


def send_message():
    """Send a message to the server to be broadcast"""

    while True:
        message = str(input(""))
        client_soc.send(message.encode(ENCODER))


def receive_message():
    """Receive an incoming message from the server"""

    while True:
        try:
            ## Receive an incoming message from the server.
            message = client_soc.recv(BYTESIZE).decode(ENCODER)

            ## Check for FLAGS, else show the message
            if message == "NAME":
                name = str(input("Whats your name? "))
                client_soc.send(name.encode(ENCODER))

            else:
                print(f"{message}")

        except:
            ## An error occurred
            print("\n\nAn error occurred...\n" "when trying to receive a message...\n" "Closing the connection...")
            client_soc.close()
            break


## Create threads to continuously send and receive messages
receive_thread = threading.Thread(target=receive_message)
send_thread = threading.Thread(target=send_message)

## Start client
receive_thread.start()
send_thread.start()
