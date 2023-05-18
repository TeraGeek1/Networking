# Json Server
import socket as soc
import json

# Create a dict to represent a message packet holding all message info
message_packet = {
    "flag": "MESSAGE",
    "name": "Mike",
    "message": "Hi there every one",
    "color": "#00ff3f",
}

# Lets look at the original dict
print()
print(message_packet)
print(type(message_packet))
print()


# # You can't directly encode a dict with .encode
# print(message_packet.encode("utf-8"))
# print(type(message_packet.encode("utf-8")))


# Turn the dict into a string using Json
message_json = json.dumps(message_packet)

print(message_json)
print(type(message_json))
print()


# Now we can encode the string representation of the dict
print(message_json.encode("utf-8"))
print(type(message_json.encode("utf-8")))
print()


# Create our client socket
server_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
server_soc.bind((soc.gethostbyname(soc.gethostname()), 12345))
server_soc.listen()


# Create a infinite while loop to accept ANY incoming connections
while True:
    client_soc, client_addr = server_soc.accept()
    print(f"Connected to {client_addr}\n")

    # Send the encoded message to the client
    client_soc.send(message_json.encode("utf-8"))

    # Close the connection
    server_soc.close()
    break
