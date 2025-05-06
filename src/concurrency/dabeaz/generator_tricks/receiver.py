import socket

from gen_pickle import gen_unpickle


def receive_from(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    c, a = s.accept()
    for item in gen_unpickle(c.makefile("rb")):
        yield item
    c.close()


if __name__ == "__main__":
    for r in receive_from(("", 15_000)):
        print(r)
