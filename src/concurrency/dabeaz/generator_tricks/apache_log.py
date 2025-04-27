import re
from typing import Any, Dict, Generator, Iterable

from field_map import field_map


def apache_log(lines: Iterable[str]):
    log_pattern = re.compile(
        r"(\S+) (\S+) (\S+) \[(.*?)\] " r'"(\S+) (\S+) (\S+)" (\S+) (\S+)'
    )
    groups = (log_pattern.match(line) for line in lines)
    tuples = (g.groups() for g in groups if g)

    col_names = (
        "host",
        "referrer",
        "user",
        "datetime",
        "method",
        "request",
        "protocol",
        "status",
        "bytes",
    )
    log_dicts: Generator[Dict[str, Any], None, None] = (
        dict(zip(col_names, t)) for t in tuples
    )
    log_dicts = field_map(
        log_dicts, "bytes", lambda s: int(s) if s != "-" else 0
    )
    log_dicts = field_map(log_dicts, "status", int)
    return log_dicts


if __name__ == "__main__":
    from gen_file_utils import lines_from_dir

    lines = lines_from_dir("access-log*", "www")
    log = apache_log(lines)

    for row in log:
        print(row)
