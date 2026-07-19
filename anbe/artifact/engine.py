#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
import shutil

from ..constants import DOWNLOADS


class ArtifactEngine:

    def detect(self, ctx):

        apk = (
            ctx.path
            / "android"
            / "app"
            / "build"
            / "outputs"
            / "apk"
            / "debug"
            / "app-debug.apk"
        )

        if apk.exists():

            ctx.artifacts.append(
                apk
            )

            ctx.log(
                "APK detected"
            )

    def export(self, ctx):

        DOWNLOADS.mkdir(
            parents=True,
            exist_ok=True
        )

        for artifact in ctx.artifacts:

            dst = DOWNLOADS / "anbe-build.apk"

            shutil.copy2(
                artifact,
                dst
            )

            ctx.exports.append(
                dst
            )

            ctx.log(
                "APK exported"
            )

