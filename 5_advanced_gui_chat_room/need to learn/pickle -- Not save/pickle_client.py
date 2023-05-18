## Pickle client
import socket as soc
import pickle


# Create the socket
client_soc = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
client_soc.connect((soc.gethostbyname(soc.gethostname()), 12345))


# receive the pickled list from the server
pickled_list = client_soc.recv(1024)

print(pickled_list)
print(type(pickled_list))


# You cannot decode using .decode, we will use pickle
unpickled_list = pickle.loads(pickled_list)

print(unpickled_list)
print(type(unpickled_list))
