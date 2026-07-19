#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
from .utils import save_json, timestamp


class Reporter:


    def create(self,ctx):

        report = {

            "schema":
            "anbe.report.v1",

            "created":
            datetime.now().isoformat(),

            "project":
            str(ctx.project),

            "profile":
            ctx.profile,

            "runtime":
            ctx.runtime,

            "workspace":
            ctx.workspace,

            "commands":
            ctx.commands,

            "logs":
            ctx.logs,

            "artifact":
            ctx.artifact,

            "success":
            not ctx.failed
        }


        filename = (
            "reports/build-"
            + timestamp()
            + ".json"
        )


        save_json(
            filename,
            report
        )


        return filename

