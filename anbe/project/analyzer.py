#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


class ProjectAnalyzer:


    def analyze(self, ctx):

        root = Path(ctx.path)


        analysis = {

            "root":
            str(root),

            "name":
            root.name,

            "framework":
            ctx.project.get(
                "framework",
                []
            ),

            "platform":
            ctx.project.get(
                "platform",
                "unknown"
            ),

            "target":
            ctx.project.get(
                "target",
                "APK"
            )

        }


        ctx.project.update(
            analysis
        )


        print(
            "[✓] Project analysis complete"
        )


        return analysis

