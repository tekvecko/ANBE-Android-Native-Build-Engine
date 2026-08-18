#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
from datetime import datetime

from .jsonutil import dumps


class BuildManifest:
    """
    Build-level ANBE manifest.

    This is NOT AndroidManifest.xml analysis.
    It describes one ANBE build and its outputs.
    """

    def create(self, ctx):

        manifest = {
            "schema": "anbe.build.manifest.v1",
            "created": datetime.now(),
            "project": ctx.project,
            "profile": ctx.profile,
            "recipe": ctx.recipe,
            "artifacts": ctx.artifacts,
            "exports": ctx.exports,
        }

        out = Path("reports")

        out.mkdir(
            parents=True,
            exist_ok=True
        )

        file = out / (
            "build-manifest-"
            +
            datetime.now().strftime(
                "%Y%m%d-%H%M%S"
            )
            +
            ".json"
        )

        file.write_text(
            dumps(
                manifest,
                indent=2
            )
        )

        ctx.meta["build_manifest"] = str(file)

        ctx.log(
            "Build manifest created"
        )

        return ctx


# Transitional compatibility.
#
# Old code imports:
#
#     from anbe.manifest import Manifest
#
# New code should eventually use:
#
#     from anbe.build_manifest import BuildManifest
#
Manifest = BuildManifest

