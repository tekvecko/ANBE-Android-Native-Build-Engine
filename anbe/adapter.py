#!/usr/bin/env python3


class RecipeAdapter:


    def adapt(self, ctx):

        steps = ctx.recipe.get(
            "steps",
            []
        )

        adapted=[]

        for step in steps:


            if "sudo apt-get update" in step:

                adapted.append(
                    "pkg update && pkg install -y libwebp"
                )

                ctx.log(
                    "[patch] apt -> pkg"
                )

                continue


            if "capacitor-assets" in step:

                adapted.append(
                    "echo 'skip capacitor-assets (sharp unsupported on android-arm64)'"
                )

                adapted.append(
                    "mkdir -p android/app/src/main/res && cp assets/icon.png android/app/src/main/res/icon.png"
                )

                ctx.log(
                    "[patch] capacitor-assets bypass"
                )

                continue


            adapted.append(step)


        ctx.recipe["steps"]=adapted

        return ctx
