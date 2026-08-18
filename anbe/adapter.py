#!/usr/bin/env python3

from .recipe.step import RecipeStep


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
                    )
                )

                ctx.log(
                    "[patch] capacitor-assets bypass"
                )

                continue

            adapted.append(
                step
            )

        ctx.recipe[
            "steps"
        ] = adapted

        return ctx
