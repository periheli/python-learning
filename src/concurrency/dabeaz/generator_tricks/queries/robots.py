if __name__ == "__main__":
    import socket

    from apache_log import apache_log
    from gen_file_utils import lines_from_dir

    lines = lines_from_dir("access-log*", "www")
    log = apache_log(lines)

    addrs = {row["host"] for row in log if "robots.txt" in row["request"]}

    for addr in addrs:
        try:
            print(socket.gethostbyaddr(addr)[0])
        except socket.herror:
            print(addr)
