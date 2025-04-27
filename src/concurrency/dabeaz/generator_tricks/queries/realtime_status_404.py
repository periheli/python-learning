import os
import sys

if __name__ == "__main__":
    from apache_log import apache_log
    from follow import follow

    log_file = open("logs/realtime-access.log")
    assert os.path.isfile(log_file.name), "Log file does not exist"
    lines = follow(log_file)
    log = apache_log(lines)

    status_404 = (row["request"] for row in log if row["status"] == 404)

    for req in status_404:
        print(req)
