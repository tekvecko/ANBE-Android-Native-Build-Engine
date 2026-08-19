#!/usr/bin/env python3

import json
from pathlib import Path


class PackageManagerResolver:

    SUPPORTED = (
        "npm",
        "pnpm",
        "yarn",
        "bun",
    )


    def package(self, project):

        project = Path(
            project
        )

        package_file = (
            project
            /
            "package.json"
        )

        if not package_file.exists():

            return {}

        try:

            return json.loads(
                package_file.read_text()
            )

        except Exception:

            return {}


    def declared(self, project):

        package = self.package(
            project
        )

        value = str(
            package.get(
                "packageManager",
                ""
            )
            or
            ""
        ).strip()

        if not value:

            return (
                None,
                None,
            )

        if "@" in value:

            name, version = (
                value.split(
                    "@",
                    1,
                )
            )

        else:

            name = value
            version = None

        name = (
            name.strip()
            .lower()
        )

        if version:

            version = (
                version.split(
                    "+",
                    1,
                )[0]
                .strip()
            )

        return (
            name,
            version,
        )


    def detect(self, project):

        project = Path(
            project
        )

        declared, version = (
            self.declared(
                project
            )
        )

        if declared in self.SUPPORTED:

            return {
                "name":
                declared,

                "version":
                version,

                "source":
                "packageManager",
            }

        lockfiles = (
            (
                "pnpm-lock.yaml",
                "pnpm",
            ),
            (
                "yarn.lock",
                "yarn",
            ),
            (
                "bun.lockb",
                "bun",
            ),
            (
                "bun.lock",
                "bun",
            ),
            (
                "package-lock.json",
                "npm",
            ),
            (
                "npm-shrinkwrap.json",
                "npm",
            ),
        )

        for filename, manager in lockfiles:

            if (
                project
                /
                filename
            ).exists():

                return {
                    "name":
                    manager,

                    "version":
                    None,

                    "source":
                    filename,
                }

        return {
            "name":
            "npm",

            "version":
            None,

            "source":
            "default",
        }


    def commands(
        self,
        project
    ):

        info = self.detect(
            project
        )

        manager = info[
            "name"
        ]

        if manager == "pnpm":

            return {
                "install":
                "pnpm install",

                "build":
                "pnpm run build",

                "capacitor":
                "pnpm exec cap sync android",
            }

        if manager == "yarn":

            return {
                "install":
                "yarn install",

                "build":
                "yarn build",

                "capacitor":
                "yarn exec cap sync android",
            }

        if manager == "bun":

            return {
                "install":
                "bun install",

                "build":
                "bun run build",

                "capacitor":
                "bunx cap sync android",
            }

        return {
            "install":
            "npm install",

            "build":
            "npm run build",

            "capacitor":
            "npx cap sync android",
        }


    def executable(
        self,
        project
    ):

        return self.detect(
            project
        )[
            "name"
        ]
