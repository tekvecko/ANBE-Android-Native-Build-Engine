#!/data/data/com.termux/files/usr/bin/python3

import json

from pathlib import Path
from datetime import datetime


def _convert(obj):

    if isinstance(obj, Path):

        return str(obj)


    if isinstance(obj, datetime):

        return obj.isoformat()

    if isinstance(obj, dict):

        return {

            k: _convert(v)

            for k, v in obj.items()

        }

    if isinstance(obj, list):

        return [

            _convert(i)

            for i in obj

        ]

    return obj


def dumps(data, **kw):

    return json.dumps(

        _convert(data),

        **kw

    )

