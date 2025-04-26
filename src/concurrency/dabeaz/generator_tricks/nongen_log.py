with open("big_access.log") as f:
    total = 0
    for line in f:
        bytes_sent = line.rsplit(None, 1)[1]
        if bytes_sent != "-":
            total += int(bytes_sent)
    print("total", total)
