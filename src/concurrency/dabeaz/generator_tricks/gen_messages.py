import socket
from typing import Any


def receive_messages(addr: tuple[Any, ...] | str, maxsize: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    while True:
        msg = s.recvfrom(maxsize)
        yield msg


if __name__ == "__main__":
    for msg, addr in receive_messages(("", 10000), 1024):
        print("Got message from", addr)
        print(msg.decode())
