#!/usr/bin/env python3

from pathlib import Path
import subprocess
import tempfile


class SourceFetcher:


    def fetch(self,source):


        if source.startswith(
            "http"
        ):

            return self.git_clone(
                source
            )


        return Path(
            source
        ).expanduser()



    def git_clone(self,url):


        target=Path(
            tempfile.mkdtemp(
                prefix="anbe-git-"
            )
        )


        subprocess.run(

            [
                "git",
                "clone",
                url,
                str(target)
            ],

            check=True

        )


        return target

