#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
import json

from .constants import CACHE


class BuildCache:

    def load(self, ctx):

        CACHE.mkdir(
            exist_ok=True
        )

        file = CACHE / "cache.json"

        if file.exists():

            ctx.cache = json.loads(
                file.read_text()
            )

            ctx.log(
                "Build cache loaded"
            )

        else:

            ctx.cache = {}

            ctx.info(
                "New build cache"
            )

    def save(self, ctx):

        file = CACHE / "cache.json"

        file.write_text(

            json.dumps(
                ctx.cache,
                indent=2
            )

        )

