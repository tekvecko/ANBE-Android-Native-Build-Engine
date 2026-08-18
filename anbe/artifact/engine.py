#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
import shutil

from ..constants import DOWNLOADS


class ArtifactEngine:

    def expected_artifact(
        self,
        ctx
    ):

        spec = ctx.recipe.get(
            "artifact"
        )

        if not isinstance(
            spec,
            dict
        ):
            return None

        path = spec.get(
            "path"
        )

        if not path:
            return None

        artifact = Path(
            path
        )

        if not artifact.is_absolute():

            artifact = (
                Path(ctx.path)
                /
                artifact
            )

        return artifact


    def detect(self, ctx):

        project = Path(
            ctx.path
        )

        candidates = []

        expected = self.expected_artifact(
            ctx
        )

        if expected is not None:

            candidates.append(
                expected
            )

        candidates.extend([
            (
                project
                / "app"
                / "build"
                / "outputs"
                / "apk"
                / "debug"
                / "app-debug.apk"
            ),
            (
                project
                / "android"
                / "app"
                / "build"
                / "outputs"
                / "apk"
                / "debug"
                / "app-debug.apk"
            ),
        ])

        apk = None

        seen = set()

        for candidate in candidates:

            candidate = Path(
                candidate
            )

            key = str(
                candidate
            )

            if key in seen:
                continue

            seen.add(
                key
            )

            if (
                candidate.exists()
                and
                candidate.is_file()
            ):

                apk = candidate
                break

        if apk is None:

            for item in project.rglob(
                "*.apk"
            ):

                if item.is_file():

                    apk = item
                    break

        if apk is not None:

            if apk not in ctx.artifacts:

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

        return ctx


    def export(self, ctx):

        DOWNLOADS.mkdir(
            parents=True,
            exist_ok=True
        )

        for artifact in ctx.artifacts:

            artifact = Path(
                artifact
            )

            if not artifact.exists():

                raise RuntimeError(
                    f"Artifact missing before export: {artifact}"
                )

            dst = (
                DOWNLOADS
                / "anbe-build.apk"
            )

            shutil.copy2(
                artifact,
                dst
            )

            if dst not in ctx.exports:

                ctx.exports.append(
                    dst
                )

            ctx.log(
                f"APK exported: {dst}"
            )

        return ctx
