#!/data/data/com.termux/files/usr/bin/python3

from anbe.plugin import BasePlugin


class Plugin(BasePlugin):

    name = "android"

    def detect(self, ctx):

        return self.exists(
            ctx,
            "android"
        )

    def prepare(self, ctx):

        ctx.runtime["android"] = True

        ctx.log(
            "Android environment prepared"
        )

        return True

