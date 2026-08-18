#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path

from .core.context import BuildContext
from .pipeline_factory import PipelineFactory


class Builder:

    def build(
        self,
        path,
        build_mode="debug",
        artifact_format="apk",
    ):

        ctx = BuildContext(
            Path(path).expanduser()
        )

        if build_mode not in (
            "debug",
            "release",
        ):

            raise ValueError(
                "Unsupported build mode: "
                + str(build_mode)
            )

        if artifact_format not in (
            "apk",
            "aab",
        ):

            raise ValueError(
                "Unsupported artifact format: "
                + str(artifact_format)
            )

        if (
            build_mode == "debug"
            and
            artifact_format == "aab"
        ):

            raise ValueError(
                "AAB output requires release mode"
            )

        ctx.build_mode = build_mode
        ctx.artifact_format = artifact_format

        pipeline = (
            PipelineFactory()
            .create()
        )

        pipeline.run(
            ctx
        )

        return ctx
