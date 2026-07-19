#!/usr/bin/env python3


from pathlib import Path



class ProfileEngine:



    def detect(self,ctx):


        root=Path(
            ctx.path
        )


        profile={

            "platform":
            "unknown",

            "mode":
            "debug",

            "artifact":
            "unknown",

            "environment":
            "termux"

        }



        if (
            root/"android"
        ).exists():


            profile["platform"]="android"


            profile["artifact"]="apk"



        if (
            root/"package.json"
        ).exists():


            profile["language"]="javascript"



        if (
            root/"capacitor.config.json"
        ).exists():


            profile["framework"]="capacitor"



        if (
            root/"vite.config.js"
        ).exists():


            profile["builder"]="vite"



        ctx.profile=profile



        ctx.log(
            "[✓] Build profile detected"
        )


        return ctx

