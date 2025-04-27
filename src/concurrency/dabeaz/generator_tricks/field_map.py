from typing import Any, Callable, Dict, Generator, Iterable


def field_map(
    dict_seq: Iterable[Dict[str, Any]],
    field: str,
    converter: Callable[[str], Any],
):
    for d in dict_seq:
        d[field] = converter(d[field])
        yield d


if __name__ == "__main__":
    import re
    from pathlib import Path

    from gen_file_utils import gen_cat, gen_open

    log_names = Path("www").rglob(("access-log*"))
    log_files = gen_open(log_names)
    log_lines = gen_cat(log_files)

    log_pattern = re.compile(
        r"(\S+) (\S+) (\S+) \[(.*?)\] " r'"(\S+) (\S+) (\S+)" (\S+) (\S+)'
    )
    groups = (log_pattern.match(line) for line in log_lines)
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

    for row in log_dicts:
        print(row)
