#!/usr/bin/env python3

import re
import shutil
from pathlib import Path

from .host_environment import HostEnvironment


class ProtobufCompatibility:

    def __init__(
        self,
        host_environment=None,
    ):

        self.host_environment = (
            host_environment
            or
            HostEnvironment()
        )


    def system_protoc(
        self,
    ):

        return shutil.which(
            "protoc"
        )


    def protobuf_files(
        self,
        project,
    ):

        project = Path(
            project
        )

        files = []

        for pattern in (
            "*.gradle",
            "*.gradle.kts",
        ):

            for path in project.rglob(
                pattern
            ):

                try:

                    text = path.read_text(
                        errors="ignore"
                    )

                except Exception:

                    continue

                if (
                    "protobuf"
                    not in text
                    or
                    "protoc"
                    not in text
                ):

                    continue

                files.append(
                    path
                )

        return files


    def uses_protoc_artifact(
        self,
        path,
    ):

        text = Path(
            path
        ).read_text(
            errors="ignore"
        )

        return (
            re.search(
                (
                    r"protoc\s*\{"
                    r"[\s\S]*?"
                    r"artifact\s*="
                ),
                text,
            )
            is not None
        )


    def replace_protoc_artifact(
        self,
        path,
        protoc,
    ):

        path = Path(
            path
        )

        text = path.read_text(
            errors="ignore"
        )

        pattern = re.compile(
            (
                r"(protoc\s*\{"
                r"[\s\S]*?)"
                r"artifact\s*=\s*[^\n]+"
            ),
        )

        replacement = (
            r'\1path = "'
            +
            str(protoc)
            +
            '"'
        )

        updated, count = pattern.subn(
            replacement,
            text,
            count=1,
        )

        if (
            count != 1
            or
            updated == text
        ):

            return False

        path.write_text(
            updated
        )

        return True


    def inspect(
        self,
        project,
    ):

        host = (
            self.host_environment
            .inspect()
        )

        protoc = self.system_protoc()

        files = []

        for path in self.protobuf_files(
            project
        ):

            if self.uses_protoc_artifact(
                path
            ):

                files.append(
                    str(path)
                )

        return {
            "host":
            host,

            "protoc":
            protoc,

            "files":
            files,

            "needs_repair":
            bool(
                host.get(
                    "termux"
                )
                and
                host.get(
                    "android"
                )
                and
                protoc
                and
                files
            ),
        }


    def repair(
        self,
        project,
    ):

        before = self.inspect(
            project
        )

        actions = []

        if before[
            "needs_repair"
        ]:

            for value in before[
                "files"
            ]:

                path = Path(
                    value
                )

                if self.replace_protoc_artifact(
                    path,
                    before[
                        "protoc"
                    ],
                ):

                    actions.append({
                        "type":
                        "protobuf_protoc_path",

                        "file":
                        str(path),

                        "to":
                        before[
                            "protoc"
                        ],
                    })

        after = self.inspect(
            project
        )

        return {
            "before":
            before,

            "after":
            after,

            "actions":
            actions,

            "changed":
            bool(actions),
        }
