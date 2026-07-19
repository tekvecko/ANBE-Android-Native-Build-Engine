#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path

from .constants import RUNTIME


class AAPT2Manager:


    def apply(self, ctx):

        aapt2 = (
            RUNTIME /
            "bin" /
            "aapt2"
        )


        if aapt2.exists():

            ctx.runtime["aapt2"] = str(
                aapt2
            )

            ctx.log(
                "AAPT2 override applied"
            )

            return True


        return False

