# Char Server side
import socket as soc

# Define constant vars
HOST_IP = soc.gethostbyname(soc.gethostname())
HOST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024


# Setup server socket
server_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)  # Create server socket
server_soc.bind((HOST_IP, HOST_PORT))  # Bind the socket to a IP and Port
server_soc.listen()  # Listen for connection attempts

# Accept any incoming connection and let them know that thy are connected
print(f"\nThe Server is running as {HOST_IP}:{HOST_PORT}...\n")
client_soc, client_addr = server_soc.accept()
client_soc.send(f"You are connected to {HOST_IP}:{HOST_PORT}...".encode(ENCODER))


while True:
    message = client_soc.recv(BYTESIZE).decode(ENCODER)

    if message == "QUIT":
        client_soc.send("QUIT".encode(ENCODER))
        print(f"\nEnding the chat...goodbye")
        break

    print(f"{message}")
    my_message = str(input("Message: "))
    client_soc.send(my_message.encode(ENCODER))

server_soc.close()
