# Chat client side
import socket as soc

# Def const vars
# DEST_IP = soc.gethostbyname(soc.gethostname()) # Connect to local server
DEST_IP = soc.gethostbyname("JHAAN-PC")  # Connect to server on my other machine
DEST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

# Setup client socket
client_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)  # Create the client socket IPv4 and TCP
client_soc.connect((DEST_IP, DEST_PORT))  # Try to connect to the server

while True:
    message = client_soc.recv(BYTESIZE).decode(ENCODER)

    if message == "QUIT":
        client_soc.send("QUIT".encode(ENCODER))
        print(f"\nEnding the chat...goodbye!")
        break

    print(f"{message}")
    my_message = str(input("Message: "))
    client_soc.send(my_message.encode(ENCODER))


client_soc.close()
