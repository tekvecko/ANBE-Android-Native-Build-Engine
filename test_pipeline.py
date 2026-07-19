from pathlib import Path

from anbe.context import BuildContext
from anbe.pipeline_factory import PipelineFactory


ctx = BuildContext(
    Path.home()
)

pipeline = PipelineFactory().create()

pipeline.run(ctx)

print("Pipeline smoke test OK")
