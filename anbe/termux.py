#!/usr/bin/env python3

import os
import shutil


class TermuxManager:


    def detect(self,ctx):

        prefix=os.environ.get(
            "PREFIX",
            ""
        )


        if "com.termux" in prefix:

            ctx.runtime[
                "environment"
            ]="termux"


            ctx.log(
                "[✓] Termux detected"
            )

            return True


        return False



    def tools(self,ctx):

        tools=[

            "node",
            "npm",
            "java",
            "gradle"

        ]


        result={}


        for tool in tools:

            result[tool]=bool(
                shutil.which(tool)
            )


        ctx.runtime[
            "tools"
        ]=result


        return ctx

