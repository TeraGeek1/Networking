# Json Client
import socket as soc
import json

# Create a client socket
client_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
client_soc.connect((soc.gethostbyname(soc.gethostname()), 12345))


# Receive the ENCODED Json string
message_json = client_soc.recv(1024)
# You don't have to decode the message, BECAUSE json.loads automatically decodes the message
# You still need to encode

# print the original state
print(f"\n{message_json}")
print(f"\n{type(message_json)}")


# Convert the Json to a dict class
message_packet = json.loads(message_json)

# print the message packet as a dict
print(f"\n{message_packet}")
print(f"\n{type(message_packet)}")

# Our new object is indeed a dict
print()
for (key, value) in message_packet.items():
    print(f"{key}: {value}")

client_soc.close()
