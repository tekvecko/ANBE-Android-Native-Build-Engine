#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


class BasePlugin:

    name = "base"

    def root(self, ctx):

        return Path(ctx.path)

    def exists(self, ctx, *parts):

        return (self.root(ctx).joinpath(*parts)).exists()

    def detect(self, ctx):

        raise NotImplementedError

    def prepare(self, ctx):

        return True

