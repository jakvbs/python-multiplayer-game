import pickle
import socket
from typing import Any


class Network:
    def __init__(self, server: str = "127.0.1.1", port: int = 5000) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_player(self) -> int:
        return int(self.p)

    def connect(self) -> Any:
        self.client.connect(self.addr)
        result = self.client.recv(2048).decode()
        return result

    def send(self, data: str) -> Any:
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 2))
        except socket.error as e:
            return str(e)
