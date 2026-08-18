#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path


class AndroidToolchain:

    def __init__(self):

        runtime_root = os.environ.get(
            "ANBE_RUNTIME",
            str(
                Path.home()
                / "ANBE-Runtime-Pack-v0.1"
            )
        )

        prefix = os.environ.get(
            "PREFIX",
            "/data/data/com.termux/files/usr"
        )

        self.runtime = (
            Path(runtime_root)
            / "bin"
        )

        self.prefix_bin = (
            Path(prefix)
            / "bin"
        )


    def valid_arm64(self, path):

        path = Path(path)

        if not path.exists():
            return False

        try:

            out = subprocess.check_output(
                [
                    "file",
                    str(path)
                ],
                text=True,
                stderr=subprocess.DEVNULL
            )

        except Exception:
            return False

        return (
            "ARM aarch64" in out
            or
            "ARM64" in out
        )


    def get(self, name):

        candidates = [
            self.runtime / name,
            self.prefix_bin / name,
            Path("/usr/local/bin") / name,
        ]

        for candidate in candidates:

            if (
                candidate.exists()
                and
                candidate.is_file()
                and
                self.valid_arm64(candidate)
            ):
                return candidate.resolve()

        return None


    def resolve(self):

        return {
            "aapt2": self.get("aapt2"),
            "aidl": self.get("aidl"),
            "zipalign": self.get("zipalign"),
            "apksigner": self.get("apksigner"),
        }
