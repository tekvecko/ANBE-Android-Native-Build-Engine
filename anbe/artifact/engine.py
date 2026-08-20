#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
import re
import shutil

from ..constants import DOWNLOADS


class ArtifactEngine:

    def repository_name(
        self,
        ctx,
    ):

        project = Path(
            ctx.path
        )

        git_config = (
            project
            /
            ".git"
            /
            "config"
        )

        if git_config.exists():

            try:

                text = git_config.read_text(
                    errors="ignore"
                )

            except Exception:

                text = ""

            remote = re.search(
                r'url\s*=\s*(.+)',
                text,
            )

            if remote:

                url = (
                    remote.group(1)
                    .strip()
                    .rstrip("/")
                )

                name = re.split(
                    r"[/\\\\:]",
                    url,
                )[-1]

                if name.endswith(
                    ".git"
                ):

                    name = name[:-4]

                name = self.sanitize_name(
                    name
                )

                if name:

                    return name

        return self.sanitize_name(
            project.name
        )


    def sanitize_name(
        self,
        value,
    ):

        value = str(
            value
            or
            ""
        ).strip()

        value = re.sub(
            r"[^A-Za-z0-9._-]+",
            "-",
            value,
        )

        value = re.sub(
            r"-+",
            "-",
            value,
        )

        return value.strip(
            ".-_"
        )


    def export_name(
        self,
        ctx,
        artifact,
    ):

        artifact = Path(
            artifact
        )

        project_name = (
            self.repository_name(
                ctx
            )
            or
            "anbe-build"
        )

        mode = getattr(
            ctx,
            "build_mode",
            "debug"
        )

        if mode == "release":

            return (
                project_name
                +
                "-release"
                +
                artifact.suffix.lower()
            )

        return (
            project_name
            +
            artifact.suffix.lower()
        )


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


    def detect(
        self,
        ctx
    ):

        project = Path(
            ctx.path
        )

        expected = (
            self.expected_artifact(
                ctx
            )
        )

        artifact = None

        if (
            expected is not None
            and
            expected.exists()
            and
            expected.is_file()
        ):

            artifact = expected

        if artifact is None:

            patterns = [
                "*.apk",
                "*.aab",
            ]

            matches = []

            for pattern in patterns:

                matches.extend(
                    item
                    for item
                    in project.rglob(
                        pattern
                    )
                    if item.is_file()
                )

            matches.sort(
                key=lambda item:
                item.stat().st_mtime,
                reverse=True
            )

            if matches:

                artifact = (
                    matches[0]
                )

        if artifact is None:

            ctx.log(
                "Build artifact not produced"
            )

            return ctx

        if artifact not in (
            ctx.artifacts
        ):

            ctx.artifacts.append(
                artifact
            )

        ctx.log(
            "Artifact detected: "
            +
            str(artifact)
        )

        return ctx


    def export(
        self,
        ctx
    ):

        DOWNLOADS.mkdir(
            parents=True,
            exist_ok=True
        )

        mode = getattr(
            ctx,
            "build_mode",
            "debug"
        )

        for artifact in (
            ctx.artifacts
        ):

            artifact = Path(
                artifact
            )

            if not artifact.exists():

                raise RuntimeError(
                    "Artifact missing before export: "
                    +
                    str(artifact)
                )

            suffix = (
                artifact.suffix.lower()
            )

            if suffix not in (
                ".apk",
                ".aab",
            ):

                raise RuntimeError(
                    "Unsupported artifact type: "
                    +
                    suffix
                )

            name = self.export_name(
                ctx,
                artifact,
            )

            dst = (
                DOWNLOADS
                /
                name
            )

            shutil.copy2(
                artifact,
                dst
            )

            if dst not in (
                ctx.exports
            ):

                ctx.exports.append(
                    dst
                )

            ctx.log(
                "Artifact exported: "
                +
                str(dst)
            )

        return ctx
