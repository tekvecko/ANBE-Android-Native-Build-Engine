#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


class GradleManager:


    def apply(self, ctx):

        root = Path(
            ctx.path
        )


        android = (
            root /
            "android"
        )


        ctx.runtime["gradle"] = str(
            android
        )


        ctx.log(
            "Gradle path configured"
        )

