#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
import shutil

from ..constants import DOWNLOADS


class ArtifactEngine:

    def detect(self, ctx):

        candidates = [
            Path(ctx.path) / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk",
            Path(ctx.path) / "android" / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk",
        ]

        apk = None

        for candidate in candidates:
            if candidate.exists():
                apk = candidate
                break

        if not apk:
            for item in Path(ctx.path).rglob("*.apk"):
                apk = item
                break

        if apk:

            ctx.artifacts.append(
                apk
            )

            ctx.log(
                f"APK detected: {apk}"
            )

        else:

            ctx.log(
                "APK not produced"
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
                f"APK exported: {dst}"
            )
