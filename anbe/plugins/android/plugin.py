#!/data/data/com.termux/files/usr/bin/python3

from anbe.plugin import BasePlugin


class Plugin(BasePlugin):

    name = "android"

    def detect(self, ctx):

        root = ctx.path

        android_files = [
            "build.gradle",
            "build.gradle.kts",
            "settings.gradle",
            "settings.gradle.kts",
            "gradlew"
        ]

        return any(
            (root / f).exists()
            for f in android_files
        )


    def prepare(self, ctx):

        ctx.runtime["android"] = True

        ctx.log(
            "Android environment prepared"
        )

        return True

