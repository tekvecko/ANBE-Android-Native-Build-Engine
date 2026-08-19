#!/usr/bin/env python3

import os
import platform
import sys


class HostEnvironment:

    def inspect(self):

        prefix = os.environ.get(
            "PREFIX",
            ""
        )

        termux = (
            "com.termux"
            in prefix
            or
            "com.termux"
            in sys.executable
        )

        system = (
            platform.system()
            .lower()
        )

        machine = (
            platform.machine()
            .lower()
        )

        android = (
            termux
            or
            system == "android"
            or
            "ANDROID_ROOT"
            in os.environ
        )

        arm64 = (
            machine
            in (
                "aarch64",
                "arm64",
            )
        )

        return {
            "termux":
            termux,

            "android":
            android,

            "arm64":
            arm64,

            "system":
            system,

            "machine":
            machine,
        }
