import bz2
import gzip
import re
from pathlib import Path
from typing import Any, Generator, Iterable, Iterator, TextIO


def gen_find(file_pattern: str, root_dir: str | Path):
    yield from Path(root_dir).rglob(file_pattern)


def gen_open(paths: Iterable[Path]) -> Generator[TextIO, Any, None]:
    for path in paths:
        if path.suffix == ".gz":
            yield gzip.open(path, "rt")
        elif path.suffix == ".bz2":
            yield bz2.open(path, "rt")
        else:
            yield open(path, "rt")


def gen_cat(sources: Iterable[Iterable[str]]):
    for src in sources:
        yield from src


def gen_grep(pattern: str, lines: Iterable[str]):
    compiled_pat = re.compile(pattern)
    return (line for line in lines if compiled_pat.search(line))


def lines_from_dir(file_pattern: str, root_dir: str | Path):
    files = Path(root_dir).rglob(file_pattern)
    files_data = gen_open(files)
    lines = gen_cat(files_data)
    return lines
