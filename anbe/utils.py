#!/usr/bin/env python3

import json
from pathlib import Path
from datetime import datetime


def timestamp():

    return datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )


def save_json(path,data):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path,"w") as f:

        json.dump(
            data,
            f,
            indent=2
        )

    return path


def load_json(path):

    with open(path) as f:

        return json.load(f)

