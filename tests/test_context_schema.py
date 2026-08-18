from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.context import BuildContext
from anbe.core.context_schema import ContextSchema


def test_context_schema_valid():

    with TemporaryDirectory(
        prefix="anbe-context-"
    ) as tmp:

        ctx = BuildContext(
            Path(tmp)
        )

        assert (
            ContextSchema.assert_valid(
                ctx
            )
            is True
        )

        assert (
            ctx.validate()
            is True
        )


def test_context_snapshot():

    with TemporaryDirectory(
        prefix="anbe-context-snapshot-"
    ) as tmp:

        ctx = BuildContext(
            Path(tmp)
        )

        ctx.project[
            "name"
        ] = "fixture"

        ctx.meta[
            "build_id"
        ] = "test-build"

        snapshot = ctx.snapshot()

        assert (
            snapshot[
                "project"
            ][
                "name"
            ]
            ==
            "fixture"
        )

        assert (
            snapshot[
                "meta"
            ][
                "build_id"
            ]
            ==
            "test-build"
        )

        assert isinstance(
            snapshot["path"],
            str
        )


def test_context_schema_rejects_corruption():

    with TemporaryDirectory(
        prefix="anbe-context-invalid-"
    ) as tmp:

        ctx = BuildContext(
            Path(tmp)
        )

        ctx.project = "invalid"

        errors = (
            ContextSchema.validate(
                ctx
            )
        )

        assert errors

        try:

            ctx.validate()

        except TypeError:

            return

        raise AssertionError(
            "Invalid BuildContext accepted"
        )


if __name__ == "__main__":

    test_context_schema_valid()
    print("Context schema regression OK")

    test_context_snapshot()
    print("Context snapshot regression OK")

    test_context_schema_rejects_corruption()
    print("Context corruption rejection OK")
