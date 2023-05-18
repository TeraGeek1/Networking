## Pickle Server
import socket as soc
import pickle


# Create a Normal list
unpickled_list = ["dill", "bread and butter", "half-sour"]

print(unpickled_list)
print(type(unpickled_list))

# # Try to encode the list using .encode # Does not work
# trial_list = unpickled_list.encode("utf-8")
# print(trial_list)
# print(type(trial_list))

# let encode by pickling the list
pickled_list = pickle.dumps(unpickled_list)

print(pickled_list)
print(type(pickled_list))


# Create a server socket
server_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
server_soc.bind((soc.gethostbyname(soc.gethostname()), 12345))
server_soc.listen()

# listen for ever to accept ANY connection
while True:
    client_soc, client_addr = server_soc.accept()

    print(f"connected to {client_addr}...\n")

    # send the encoded list
    client_soc.send(pickled_list)  # Pickled_list is already encoded AKA a bytes object

    server_soc.close()
