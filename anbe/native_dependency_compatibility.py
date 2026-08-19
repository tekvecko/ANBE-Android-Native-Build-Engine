#!/usr/bin/env python3

import json
from pathlib import Path

from .host_environment import HostEnvironment


class NativeDependencyCompatibility:

    def __init__(
        self,
        host_environment=None,
    ):

        self.host_environment = (
            host_environment
            or
            HostEnvironment()
        )


    def package(
        self,
        project,
    ):

        path = (
            Path(project)
            /
            "package.json"
        )

        if not path.exists():

            return {}

        try:

            return json.loads(
                path.read_text()
            )

        except Exception:

            return {}


    def has_capacitor_assets(
        self,
        project,
    ):

        package = self.package(
            project
        )

        dependencies = {}

        dependencies.update(
            package.get(
                "dependencies",
                {}
            )
        )

        dependencies.update(
            package.get(
                "devDependencies",
                {}
            )
        )

        return (
            "@capacitor/assets"
            in dependencies
        )


    def workspace_file(
        self,
        project,
    ):

        path = (
            Path(project)
            /
            "pnpm-workspace.yaml"
        )

        if path.exists():

            return path

        return None


    def sharp_is_approved(
        self,
        project,
    ):

        path = self.workspace_file(
            project
        )

        if not path:

            return False

        text = path.read_text(
            errors="ignore"
        )

        return (
            "onlyBuiltDependencies:"
            in text
            and
            any(
                line.strip()
                in (
                    "- sharp",
                    "- 'sharp'",
                    '- "sharp"',
                )
                for line in text.splitlines()
            )
        )


    def remove_sharp_approval(
        self,
        project,
    ):

        path = self.workspace_file(
            project
        )

        if not path:

            return False

        lines = path.read_text(
            errors="ignore"
        ).splitlines()

        updated = []
        removed = False

        for line in lines:

            stripped = (
                line.strip()
            )

            if stripped in (
                "- sharp",
                "- 'sharp'",
                '- "sharp"',
            ):

                removed = True
                continue

            updated.append(
                line
            )

        if not removed:

            return False

        path.write_text(
            "\n".join(
                updated
            )
            +
            "\n"
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

        return {
            "host":
            host,

            "capacitor_assets":
            self.has_capacitor_assets(
                project
            ),

            "pnpm_workspace":
            (
                self.workspace_file(
                    project
                )
                is not None
            ),

            "sharp_approved":
            self.sharp_is_approved(
                project
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

        should_repair = (
            before[
                "host"
            ][
                "termux"
            ]
            and
            before[
                "host"
            ][
                "android"
            ]
            and
            before[
                "host"
            ][
                "arm64"
            ]
            and
            before[
                "capacitor_assets"
            ]
            and
            before[
                "pnpm_workspace"
            ]
            and
            before[
                "sharp_approved"
            ]
        )

        if should_repair:

            if self.remove_sharp_approval(
                project
            ):

                actions.append({
                    "type":
                    "disable_sharp_build",

                    "dependency":
                    "sharp",

                    "reason":
                    (
                        "unsupported sharp/libvips "
                        "install on Termux Android ARM64"
                    ),
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
