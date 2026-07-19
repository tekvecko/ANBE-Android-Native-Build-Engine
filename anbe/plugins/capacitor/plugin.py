#!/data/data/com.termux/files/usr/bin/python3

from anbe.plugin import BasePlugin


class Plugin(BasePlugin):

    name = "capacitor"

    def detect(self, ctx):

        return self.exists(
            ctx,
            "capacitor.config.json"
        )

    def prepare(self, ctx):

        ctx.runtime["capacitor"] = True

        ctx.log(
            "Capacitor detected"
        )

        return True

