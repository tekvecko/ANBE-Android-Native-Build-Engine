#!/usr/bin/env python3

from .recipe.step import RecipeStep
from .recipe.graph import RecipeGraph


class RecipeAdapter:

    def adapt(
        self,
        ctx
    ):

        steps = (
            RecipeStep.normalize_all(
                ctx.recipe.get(
                    "steps",
                    []
                )
            )
        )

        adapted = []

        for step in steps:

            step_type = step[
                "type"
            ]

            command = step.get(
                "command",
                ""
            )

            if (
                step_type
                ==
                "command"
                and
                "sudo apt-get update"
                in command
            ):

                adapted.append(
                    RecipeStep.command(
                        "termux-install-libwebp",
                        "pkg update && "
                        "pkg install -y libwebp",
                        depends_on=step.get(
                            "depends_on",
                            []
                        ),
                    )
                )

                ctx.log(
                    "[patch] apt -> pkg"
                )

                continue

            if (
                step_type
                ==
                "command"
                and
                "capacitor-assets"
                in command
            ):

                adapted.append(
                    RecipeStep.command(
                        "capacitor-assets-skip",
                        "echo 'skip capacitor-assets "
                        "(sharp unsupported on "
                        "android-arm64)'",
                        depends_on=step.get(
                            "depends_on",
                            []
                        ),
                    )
                )

                adapted.append(
                    RecipeStep.command(
                        "capacitor-icon-copy",
                        "mkdir -p "
                        "android/app/src/main/res "
                        "&& cp assets/icon.png "
                        "android/app/src/main/res/"
                        "icon.png",
                        depends_on=[
                            "capacitor-assets-skip"
                        ],
                    )
                )

                ctx.log(
                    "[patch] capacitor-assets bypass"
                )

                continue

            adapted.append(
                step
            )

        RecipeGraph.assert_valid(
            adapted
        )

        ctx.recipe[
            "steps"
        ] = RecipeGraph.topological_sort(
            adapted
        )

        return ctx
