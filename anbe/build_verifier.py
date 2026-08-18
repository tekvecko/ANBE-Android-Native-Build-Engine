#!/usr/bin/env python3

from pathlib import Path


class BuildVerifier:

    def verify(self, ctx):

        failures = []

        execution = getattr(
            ctx,
            "execution",
            []
        )

        for result in execution:

            if not isinstance(
                result,
                dict
            ):
                continue

            if result.get(
                "success"
            ) is False:

                failures.append(
                    "Command failed: "
                    +
                    str(
                        result.get(
                            "command",
                            "unknown"
                        )
                    )
                )

        spec = ctx.recipe.get(
            "artifact"
        )

        expected = None

        if isinstance(
            spec,
            dict
        ):

            path = spec.get(
                "path"
            )

            if path:

                expected = Path(
                    path
                )

                if not expected.is_absolute():

                    expected = (
                        Path(ctx.path)
                        /
                        expected
                    )

                if not expected.exists():

                    failures.append(
                        "Expected artifact not found: "
                        +
                        str(expected)
                    )

                elif expected.stat().st_size <= 0:

                    failures.append(
                        "Expected artifact is empty: "
                        +
                        str(expected)
                    )

        if spec and not ctx.artifacts:

            failures.append(
                "Artifact was expected but ArtifactEngine detected none"
            )

        for artifact in ctx.artifacts:

            artifact = Path(
                artifact
            )

            if not artifact.exists():

                failures.append(
                    "Detected artifact does not exist: "
                    +
                    str(artifact)
                )

            elif artifact.stat().st_size <= 0:

                failures.append(
                    "Detected artifact is empty: "
                    +
                    str(artifact)
                )

        verification = {
            "success":
            not failures,

            "artifact":
            (
                str(expected)
                if expected
                else None
            ),

            "errors":
            failures,
        }

        ctx.meta[
            "verification"
        ] = verification

        if failures:

            raise RuntimeError(
                "Build verification failed: "
                +
                "; ".join(
                    failures
                )
            )

        ctx.log(
            "Build verification passed"
        )

        return ctx
