import pickle
import socket

from broadcast import Consumer


class NetConsumer(Consumer):
    def __init__(self, addr):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(addr)

    def send(self, item):
        pickled_item = pickle.dumps(item)
        self.socket.sendall(pickled_item)

    def close(self):
        self.socket.close()


class Stat404(NetConsumer):
    def send(self, item: dict):
        if item["status"] == 404:
            super().send(item)


if __name__ == "__main__":
    from apache_log import apache_log
    from broadcast import broadcast
    from follow import follow

    lines = follow(open("logs/realtime-access.log"))
    log = apache_log(lines)
    stat_404 = Stat404(("", 15_000))
    broadcast(log, [stat_404])
