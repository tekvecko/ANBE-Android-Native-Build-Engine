#!/data/data/com.termux/files/usr/bin/python3

from anbe.plugin import BasePlugin


class Plugin(BasePlugin):

    name = "generic"

    def detect(self, ctx):

        return True

    def prepare(self, ctx):

        ctx.runtime["generic"] = True

        ctx.log(
            "Generic project"
        )

        return True

