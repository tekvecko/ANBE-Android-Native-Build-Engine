#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
from datetime import datetime

from .jsonutil import dumps


class Manifest:


    def create(self, ctx):


        manifest = {

            "schema":
            "anbe.manifest.v1",

            "created":
            datetime.now(),

            "project":
            ctx.project,

            "profile":
            ctx.profile,

            "artifacts":
            ctx.artifacts,

            "exports":
            ctx.exports

        }


        out = Path("reports")

        out.mkdir(
            exist_ok=True
        )


        file = out / (
            "manifest-"
            +
            datetime.now().strftime(
                "%Y%m%d-%H%M%S"
            )
            +
            ".json"
        )


        file.write_text(

            dumps(
                manifest,
                indent=2
            )

        )


        ctx.manifest = manifest


        ctx.log(
            "[✓] Manifest created"
        )

