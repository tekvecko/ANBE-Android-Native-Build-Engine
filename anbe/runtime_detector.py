#!/usr/bin/env python3

from pathlib import Path


class RuntimeDetector:



    def detect(self,ctx):


        packs=[


            Path(
                "~/ANBE-Runtime-Pack-v0.1"
            ).expanduser(),


            Path(
                "~/.anbe/runtime"
            ).expanduser()


        ]



        for pack in packs:


            if pack.exists():


                ctx.runtime={

                    "available":True,

                    "path":
                    str(pack)

                }


                ctx.log(
                    "[✓] Runtime detected"
                )


                return ctx



        ctx.runtime={

            "available":False

        }


        ctx.log(
            "[!] Runtime missing"
        )


        return ctx

