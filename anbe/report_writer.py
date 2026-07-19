#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
from datetime import datetime

from .jsonutil import dumps


class ReportWriter:

    def __init__(self):

        self.root = Path("reports")

        self.root.mkdir(
            exist_ok=True
        )

    def write(
        self,
        name,
        data
    ):

        file = self.root / (

            name
            + "-"
            + datetime.now().strftime(
                "%Y%m%d-%H%M%S"
            )
            + ".json"

        )

        file.write_text(

            dumps(
                data,
                indent=2
            )

        )

        return file

