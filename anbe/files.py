#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


def ensure(path):

    path = Path(path)

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


def write(path, text):

    path = Path(path)

    ensure(
        path.parent
    )

    path.write_text(text)

    return path


def read(path):

    return Path(path).read_text()

