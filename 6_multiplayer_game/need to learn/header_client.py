"""An into to using fixed length headers client"""
import socket as soc

# Create a socket
client_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
client_soc.connect((soc.gethostbyname(soc.gethostname()), 1105))


# # Cuts of the message
# message1 = client_soc.recv(8).decode("utf-8")
# print(message1)
# message2 = client_soc.recv(8).decode("utf-8")
# print(message2)


# This works but large message can still get cut of and
message1 = client_soc.recv(1024).decode("utf-8")
print(message1)
message2 = client_soc.recv(1024).decode("utf-8")
print(message2)
