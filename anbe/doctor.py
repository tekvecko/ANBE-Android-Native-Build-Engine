#!/usr/bin/env python3

import shutil


class Doctor:


    def run(self,ctx):

        tools=[

            "node",
            "npm",
            "java",
            "gradle"

        ]


        result={}


        for t in tools:

            result[t]=bool(
                shutil.which(t)
            )


        ctx.doctor=result


        missing=[

            x for x,y in result.items()
            if not y

        ]


        if missing:

            ctx.log(
                "[!] Missing tools: "
                +
                str(missing)
            )

        else:

            ctx.log(
                "[✓] Environment OK"
            )


        return ctx



