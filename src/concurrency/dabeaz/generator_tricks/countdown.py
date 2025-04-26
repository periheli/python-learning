class countdown:
    def __init__(self, start: int):
        self.start = start

    def __iter__(self):
        return countdown_iter(self.start)


class countdown_iter:
    def __init__(self, count: int):
        self.count = count

    def __next__(self):
        if self.count <= 0:
            raise StopIteration
        value = self.count
        self.count -= 1
        return value


def countdown_generator(start: int):
    print("Counting down from", start)
    while start > 0:
        yield start
        start -= 1
