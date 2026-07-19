from pathlib import Path

from anbe.context import BuildContext


ctx = BuildContext(
    Path("/tmp/project")
)


assert isinstance(
    ctx.path,
    Path
)

assert isinstance(
    ctx.project,
    dict
)

assert isinstance(
    ctx.profile,
    dict
)

assert isinstance(
    ctx.recipe,
    dict
)

assert hasattr(
    ctx,
    "aapt2"
)


print("Context contract OK")
