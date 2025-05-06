import socket

from gen_pickle import gen_pickle


def send_to(source, addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    for item in gen_pickle(source):
        s.sendall(item)
    s.close()


if __name__ == "__main__":
    from apache_log import apache_log
    from follow import follow

    lines = follow(open("logs/realtime-access.log"))
    log = apache_log(lines)
    send_to(log, ("", 15_000))
