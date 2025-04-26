with open("big_access.log") as f:
    byte_column = (line.rsplit(None, 1)[1] for line in f)
    bytes_sent = (int(x) for x in byte_column if x != "-")
    print("Total", sum(bytes_sent))
