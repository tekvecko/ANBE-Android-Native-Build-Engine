#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


class Workspace:


    def prepare(self, ctx):

        root = Path(
            ctx.path
        )


        data = {

            "root":
            str(root),

            "android":
            str(
                root / "android"
            )

        }


        ctx.workspace = data


        return data

