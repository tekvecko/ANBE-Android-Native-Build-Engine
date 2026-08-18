#!/usr/bin/env python3

from .android_toolchain import AndroidToolchain


class AAPT2Manager:

    def apply(self, ctx):

        aapt2 = AndroidToolchain().get(
            "aapt2"
        )

        if not aapt2:

            raise RuntimeError(
                "Compatible ARM64 AAPT2 executable not found"
            )

        value = str(
            aapt2
        )

        ctx.aapt2 = value

        ctx.runtime[
            "aapt2"
        ] = value

        ctx.log(
            f"AAPT2 override applied: {value}"
        )

        return ctx
