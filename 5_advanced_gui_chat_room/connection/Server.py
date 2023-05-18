"""The Connection class for the server side"""
from connection.locals import *
import socket as soc


class Connection:
    """Store pertinent info"""

    def __init__(self) -> None:
        self.host_ip = soc.gethostbyname(soc.gethostname())
        self.encoder = ENCODER
        self.bytesize = BYTESIZE

        self.client_socs = []
        self.client_ips = []
        self.baned_ips = []

        self.port: int
        self.soc: soc.socket
        self.connected: bool = False

    def reset_server(self):
        self.client_ips = []
        self.baned_ips = []

        for client_soc in self.client_socs:
            client_soc.close()
            self.client_socs.remove(client_soc)
