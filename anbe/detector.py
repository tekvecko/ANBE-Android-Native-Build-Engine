#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


class ProjectDetector:


    def detect(self, ctx):

        root = Path(ctx.path)


        project = {}


        if (
            root /
            "capacitor.config.json"
        ).exists():

            project["framework"] = [
                "Capacitor"
            ]


        if (
            root /
            "vite.config.js"
        ).exists():

            project["framework"].append(
                "Vite"
            )


        if (
            root /
            "android"
        ).exists():

            project["platform"] = "android"


        project["target"] = "APK"


        ctx.project = project


        print(
            "[✓] Project detected"
        )


        return project

