#!/usr/bin/env python3

import json
from pathlib import Path

from .host_environment import HostEnvironment


class PackageManagerResolver:

    def __init__(
        self,
        host_environment=None,
    ):

        self.host_environment = (
            host_environment
            or
            HostEnvironment()
        )


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


    def termux_android_arm64(
        self,
    ):

        host = (
            self.host_environment
            .inspect()
        )

        return (
            host.get(
                "termux"
            )
            and
            host.get(
                "android"
            )
            and
            host.get(
                "arm64"
            )
        )


    def has_dependency(
        self,
        project,
        name,
    ):

        package = self.package(
            project
        )

        for section in (
            "dependencies",
            "devDependencies",
            "optionalDependencies",
        ):

            values = package.get(
                section,
                {}
            )

            if (
                isinstance(
                    values,
                    dict
                )
                and
                name
                in values
            ):

                return True

        return False


    def lockfile_contains(
        self,
        project,
        text,
    ):

        project = Path(
            project
        )

        for name in (
            "package-lock.json",
            "npm-shrinkwrap.json",
        ):

            path = (
                project
                /
                name
            )

            if not path.exists():

                continue

            try:

                data = path.read_text(
                    errors="ignore"
                )

            except Exception:

                continue

            if text in data:

                return True

        return False


    def needs_termux_npm_compatibility(
        self,
        project,
    ):

        if not self.termux_android_arm64():

            return False

        if self.has_dependency(
            project,
            "puppeteer",
        ):

            return True

        for marker in (
            '"node_modules/lmdb"',
            '"node_modules/@parcel/watcher"',
        ):

            if self.lockfile_contains(
                project,
                marker,
            ):

                return True

        return False


    def npm_lockfile(
        self,
        project,
    ):

        project = Path(
            project
        )

        for name in (
            "package-lock.json",
            "npm-shrinkwrap.json",
        ):

            path = (
                project
                /
                name
            )

            if path.exists():

                return path

        return None


    def dependency_version(
        self,
        project,
        name,
    ):

        package = self.package(
            project
        )

        for section in (
            "dependencies",
            "devDependencies",
            "optionalDependencies",
        ):

            values = package.get(
                section,
                {}
            )

            if not isinstance(
                values,
                dict
            ):

                continue

            version = values.get(
                name
            )

            if version:

                return str(
                    version
                )

        return None


    def version_major(
        self,
        value,
    ):

        if not value:

            return None

        import re

        match = re.search(
            r"(\d+)",
            str(
                value
            ),
        )

        if not match:

            return None

        return int(
            match.group(1)
        )


    def lockfile_package_version(
        self,
        project,
        package_name,
    ):

        import json

        project = Path(
            project
        )

        for name in (
            "package-lock.json",
            "npm-shrinkwrap.json",
        ):

            path = (
                project
                /
                name
            )

            if not path.exists():

                continue

            try:

                data = json.loads(
                    path.read_text()
                )

            except Exception:

                continue

            packages = data.get(
                "packages",
                {}
            )

            entry = packages.get(
                "node_modules/"
                +
                package_name
            )

            if isinstance(
                entry,
                dict
            ):

                version = entry.get(
                    "version"
                )

                if version:

                    return str(
                        version
                    )

        return None


    def needs_legacy_openssl_provider(
        self,
        project,
    ):

        angular = self.dependency_version(
            project,
            "@angular-devkit/build-angular",
        )

        angular_major = self.version_major(
            angular
        )

        webpack = self.lockfile_package_version(
            project,
            "webpack",
        )

        webpack_major = self.version_major(
            webpack
        )

        if (
            angular_major is None
            or
            webpack_major is None
        ):

            return False

        return (
            angular_major
            <=
            12
            and
            webpack_major
            ==
            5
        )


    def build_command(
        self,
        project,
        command,
    ):

        if self.needs_legacy_openssl_provider(
            project
        ):

            return (
                "NODE_OPTIONS=--openssl-legacy-provider "
                +
                command
            )

        return command


    def npm_install_command(
        self,
        project,
    ):

        if self.needs_termux_npm_compatibility(
            project
        ):

            if self.npm_lockfile(
                project
            ):

                return (
                    "PUPPETEER_SKIP_DOWNLOAD=true "
                    "npm ci --omit=optional"
                )

            return (
                "PUPPETEER_SKIP_DOWNLOAD=true "
                "npm install --omit=optional"
            )

        return "npm install"


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
                self.build_command(
                    project,
                    "pnpm run build",
                ),

                "capacitor":
                "pnpm exec cap sync android",
            }

        if manager == "yarn":

            return {
                "install":
                "yarn install",

                "build":
                self.build_command(
                    project,
                    "yarn build",
                ),

                "capacitor":
                "yarn exec cap sync android",
            }

        if manager == "bun":

            return {
                "install":
                "bun install",

                "build":
                self.build_command(
                    project,
                    "bun run build",
                ),

                "capacitor":
                "bunx cap sync android",
            }

        return {
            "install":
            self.npm_install_command(
                project
            ),

            "build":
            self.build_command(
                project,
                "npm run build",
            ),

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
