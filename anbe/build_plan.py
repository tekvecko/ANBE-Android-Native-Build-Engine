#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
from datetime import datetime

from .jsonutil import dumps


class BuildPlan:


    def create(self, ctx):


        report = {

            "schema":
            "anbe.build.plan.v1",

            "created":
            datetime.now(),

            "project":
            ctx.project,

            "profile":
            ctx.profile,

            "recipe":
            ctx.recipe

        }


        ctx.build_plan = report


        out = Path("reports")

        out.mkdir(
            exist_ok=True
        )


        file = out / (
            "build-plan-"
            +
            datetime.now().strftime(
                "%Y%m%d-%H%M%S"
            )
            +
            ".json"
        )


        file.write_text(

            dumps(
                report,
                indent=2
            )

        )


        ctx.log(
            "[✓] Build plan generated"
        )


        return ctx

