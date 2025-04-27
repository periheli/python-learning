import os
import time
from typing import IO, TypeVar

AnyStr = TypeVar("AnyStr", bytes, str)


def follow(file: IO[AnyStr]):
    file.seek(0, os.SEEK_END)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == "__main__":
    log_file = open("logs/realtime-access.log")
    log_lines = follow(log_file)

    for line in log_lines:
        print(line, end="")
