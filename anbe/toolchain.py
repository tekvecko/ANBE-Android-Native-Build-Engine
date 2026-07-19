#!/usr/bin/env python3

from pathlib import Path
import shutil


class Toolchain:


    def scan(self,ctx):

        tools=[
            "java",
            "gradle",
            "node",
            "npm",
            "aapt2"
        ]


        result={}


        for tool in tools:

            result[tool]=shutil.which(
                tool
            )


        ctx.toolchain=result


        ctx.log(
            "[✓] Toolchain scanned"
        )


        return ctx


    def require(self,ctx):

        required=[

            "java",
            "gradle"

        ]


        missing=[]


        for item in required:

            if not ctx.toolchain.get(item):

                missing.append(item)


        if missing:

            ctx.log(
                "[!] Missing: "
                +
                str(missing)
            )

            ctx.failed=True


        return ctx

