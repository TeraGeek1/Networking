from connection.locals import *
import socket as soc


class Connection:
    """Store pertinent info"""

    def __init__(self) -> None:
        self.encoder = ENCODER
        self.bytesize = BYTESIZE

        self.name: str
        self.target_ip: str
        self.target_port: str
        self.color: str
        self.connected: bool = False

        self.client_soc: soc.socket

    def reset_client(self):
        """Reset all the old server info"""

        self.name: str
        self.target_ip: str
        self.target_port: str
        self.color: str
        self.connected = False

        self.client_soc.close()
