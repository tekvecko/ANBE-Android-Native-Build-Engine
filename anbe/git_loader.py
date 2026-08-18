#!/usr/bin/env python3

from pathlib import Path
import subprocess
import tempfile


class GitLoader:

    def load(self, source):

        if isinstance(source, Path):
            return source

        source = str(source)

        if source.startswith(
            ("http://", "https://")
        ):

            if not source.endswith(".git"):
                source = source.rstrip("/") + ".git"

            target = Path(
                tempfile.mkdtemp(
                    prefix="anbe-git-"
                )
            )

            print(
                f"[>] Cloning repository: {source}"
            )

            subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    "--recurse-submodules",
                    source,
                    str(target)
                ],
                check=True
            )

            subprocess.run(
                [
                    "git",
                    "-C",
                    str(target),
                    "submodule",
                    "update",
                    "--init",
                    "--recursive"
                ],
                check=False
            )

            return target


        return Path(source)
