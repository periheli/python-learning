import socket
from typing import Any


def receive_connections(addr: tuple[Any, ...] | str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    while True:
        client = s.accept()
        yield client


if __name__ == "__main__":
    for c, a in receive_connections(("", 9000)):
        print("Got connection from", a)
        c.send(b"Hello World\n")
        c.close()
