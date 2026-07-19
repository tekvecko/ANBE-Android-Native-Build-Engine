#!/usr/bin/env python3

from pathlib import Path
import os


class RuntimeManager:


    def inspect(self,ctx):

        base=Path(
            "~/ANBE-Runtime-Pack-v0.1"
        ).expanduser()


        runtime={}


        if base.exists():

            runtime["path"]=str(base)

            runtime["aapt2"]=str(
                base/"bin/aapt2"
            )


            ctx.log(
                "[✓] ANBE Runtime Pack found"
            )


        else:

            ctx.log(
                "[!] Runtime Pack missing"
            )


        ctx.runtime_pack=runtime


        return ctx

