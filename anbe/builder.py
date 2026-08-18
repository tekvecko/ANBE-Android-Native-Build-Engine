#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path

from .core.context import BuildContext
from .pipeline_factory import PipelineFactory


class Builder:

    def build(self, path):

        ctx = BuildContext(
            Path(path).expanduser()
        )

        pipeline = PipelineFactory().create()

        pipeline.run(ctx)

        return ctx
