#!/usr/bin/env python3


from pathlib import Path
import json



class RecipeEngine:



    def generate(self,ctx):


        project=Path(
            ctx.path
        )


        recipe={

            "schema":
            "anbe.recipe.dynamic.v1",

            "project":
            str(project),

            "steps":[],

            "artifact":
            None

        }



        if (
            project/"package.json"
        ).exists():


            recipe["steps"].append(
                "npm install"
            )



            package=json.loads(
                (
                    project/"package.json"
                ).read_text()
            )


            scripts=package.get(
                "scripts",
                {}
            )


            if "build" in scripts:


                recipe["steps"].append(
                    "npm run build"
                )



        if (
            project/"capacitor.config.json"
        ).exists():


            recipe["steps"].append(
                "npx cap sync android"
            )



        if (
            project/"android"
        ).exists():


            recipe["steps"].extend(

                [

                "android prepare",

                "gradle assembleDebug"

                ]

            )


            recipe["artifact"]={

                "type":
                "apk",

                "path":
                "android/app/build/outputs/apk/debug/app-debug.apk"

            }



        ctx.recipe=recipe


        ctx.log(
            "[✓] Dynamic recipe generated"
        )


        return ctx

