"""An into to using fixed length headers server"""
import socket as soc

# Create socket
server_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
server_soc.bind((soc.gethostbyname(soc.gethostname()), 1105))
server_soc.listen()

# Vars
message1 = "Hello we are learning more about sockets!"
message2 = "Good bye now we know about Headers!!"

while True:
    client_soc, client_addr = server_soc.accept()
    print(f"Connected to {client_addr}\n")

    # Lets try to send two messages
    client_soc.send(message1.encode("utf-8"))
    client_soc.send(message2.encode("utf-8"))
