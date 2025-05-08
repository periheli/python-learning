class Consumer:
    def __init__(self):
        self.id = id(self)

    def send(self, item):
        print(self, "got", item)

    def __str__(self):
        return f"Consumer {id(self)}"


def broadcast(source, consumers: list[Consumer]):
    for item in source:
        for c in consumers:
            c.send(item)


if __name__ == "__main__":
    from follow import follow

    c1 = Consumer()
    c2 = Consumer()
    c3 = Consumer()

    lines = follow(open("logs/realtime-access.log"))
    broadcast(lines, [c1, c2, c3])
