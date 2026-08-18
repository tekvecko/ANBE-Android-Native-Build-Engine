#!/usr/bin/env python3

from pathlib import Path
import subprocess


class AndroidToolchain:


    def __init__(self):

        self.runtime = Path(
            "/data/data/com.termux/files/home/ANBE-Runtime-Pack-v0.1/bin"
        )


    def valid_arm64(self, path):

        try:
            out = subprocess.check_output(
                ["file", str(path)],
                text=True
            )

            return "ARM aarch64" in out

        except Exception:
            return False


    def get(self, name):

        tool = self.runtime / name

        if tool.exists() and self.valid_arm64(tool):
            return tool

        termux = Path(
            "/data/data/com.termux/files/usr/bin"
        ) / name

        if termux.exists() and self.valid_arm64(termux):
            return termux

        return None


    def resolve(self):

        return {
            "aapt2": self.get("aapt2"),
            "aidl": self.get("aidl"),
            "zipalign": self.get("zipalign"),
            "apksigner": self.get("apksigner"),
        }
