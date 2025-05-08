from queue import Queue
from threading import Thread
from typing import Callable

from broadcast import Consumer


class ConsumerThread(Thread, Consumer):
    def __init__(self, target: Callable):
        super().__init__()
        self.daemon = True
        self.queue = Queue()
        self.target = target

    def send(self, item):
        self.queue.put(item)

    def generate(self):
        while True:
            item = self.queue.get()
            yield item

    def run(self):
        self.target(self.generate())


if __name__ == "__main__":
    from apache_log import apache_log
    from broadcast import broadcast
    from follow import follow

    def find_404(log):
        req_404 = (r for r in log if r["status"] == 404)
        for req in req_404:
            print(req["status"], req["datetime"], req["request"])

    def bytes_transferred(log):
        total = 0
        for req in log:
            total += req["bytes"]
            print("Total bytes:", total)

    c1 = ConsumerThread(find_404)
    c1.start()
    c2 = ConsumerThread(bytes_transferred)
    c2.start()

    lines = follow(open("logs/realtime-access.log"))
    log = apache_log(lines)
    broadcast(log, [c1, c2])
