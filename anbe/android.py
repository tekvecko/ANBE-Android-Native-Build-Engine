#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


class AndroidManager:


    def __init__(self, ctx):

        self.ctx = ctx


    @property
    def root(self):

        return Path(
            self.ctx.path
        )


    @property
    def android_dir(self):

        return (
            self.root /
            "android"
        )


    def exists(self):

        return self.android_dir.exists()


    def prepare(self):

        if self.exists():

            self.ctx.log(
                "Android project detected"
            )

            return True

        return False

