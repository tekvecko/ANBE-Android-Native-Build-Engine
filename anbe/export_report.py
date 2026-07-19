#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
from datetime import datetime

from .jsonutil import dumps


class ExportReport:


    def save(self, ctx):


        out = Path("reports")

        out.mkdir(
            exist_ok=True
        )


        report = {

            "schema":
            "anbe.export.report.v1",

            "created":
            datetime.now().isoformat(),

            "project":
            ctx.project,

            "exports":
            ctx.exports,

            "artifacts":
            ctx.artifacts

        }


        file = out / (
            "export-report-"
            +
            datetime.now().strftime(
                "%Y%m%d-%H%M%S"
            )
            +
            ".json"
            )

        file.write_text(

            dumps(
                report,
                indent=2
            )

        )


        ctx.log(
            "[✓] Export report saved"
        )

