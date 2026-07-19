#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path

from .builder import Builder
from .context_dump import ContextDump


class Orchestrator:


    def run(self, project):

        print()
        print("="*40)
        print("ANBE Autonomous Builder v1.0")
        print("="*40)


        project = Path(project)


        ctx = Builder().build(
            project
        )


        ContextDump().save(
            ctx
        )


        print()
        print("="*40)
        print("BUILD FINISHED")
        print("="*40)

        return ctx

