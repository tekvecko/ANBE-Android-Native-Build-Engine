#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
from .git_loader import GitLoader

from .builder import Builder
from .context_dump import ContextDump


class Orchestrator:


    def run(
        self,
        project,
        build_mode="debug",
        artifact_format="apk",
    ):

        print()
        print("="*40)
        print("ANBE Autonomous Builder v1.0")
        print("="*40)


        project = GitLoader().load(project)


        ctx = Builder().build(
            project,
            build_mode=build_mode,
            artifact_format=artifact_format,
        )


        ContextDump().save(
            ctx
        )


        print()
        print("="*40)
        print("BUILD FINISHED")
        print("="*40)

        return ctx

