#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path

from .jsonutil import dumps


class ContextDump:


    def save(self, ctx):

        out = Path("reports")

        out.mkdir(
            exist_ok=True
        )


        data = {

            "path":
            ctx.path,

            "project":
            ctx.project,

            "profile":
            ctx.profile,

            "recipe":
            ctx.recipe,

            "plan":
            getattr(
                ctx,
                "plan",
                {}
            ),

            "build_plan":
            getattr(
                ctx,
                "build_plan",
                {}
            ),

            "plugin":
            str(
                getattr(
                    ctx,
                    "plugin",
                    None
                )
            ),

            "runtime":
            ctx.runtime,

            "artifacts":
            ctx.artifacts,

            "exports":
            ctx.exports

        }


        file = out / "context-debug.json"


        file.write_text(

            dumps(
                data,
                indent=2
            )

        )


        print(
            "[✓] Context dump:",
            file
        )

