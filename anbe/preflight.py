#!/usr/bin/env python3

import json
import os
import shutil

from datetime import datetime
from pathlib import Path

from .android_toolchain import AndroidToolchain
from .java_resolver import JavaResolver
from .package_manager import PackageManagerResolver


class Preflight:

    def __init__(
        self,
        java_resolver=None,
        android_toolchain=None,
        package_manager_resolver=None,
        which=None,
    ):

        self.java_resolver = (
            java_resolver
            or
            JavaResolver()
        )

        self.android_toolchain = (
            android_toolchain
            or
            AndroidToolchain()
        )

        self.package_manager_resolver = (
            package_manager_resolver
            or
            PackageManagerResolver()
        )

        self.which = (
            which
            or
            shutil.which
        )


    def _check(
        self,
        checks,
        name,
        ok,
        value=None,
        required=True,
        message=None,
    ):

        item = {
            "name": name,
            "status": (
                "PASS"
                if ok
                else (
                    "FAIL"
                    if required
                    else "WARN"
                )
            ),
            "required": required,
            "value": (
                str(value)
                if value is not None
                else None
            ),
        }

        if message:
            item["message"] = message

        checks.append(
            item
        )

        return ok


    def detect_android_root(
        self,
        project
    ):

        candidates = [
            project / "android",
            project,
        ]

        indicators = [
            "gradlew",
            "build.gradle",
            "build.gradle.kts",
            "settings.gradle",
            "settings.gradle.kts",
        ]

        for candidate in candidates:

            if any(
                (
                    candidate
                    /
                    indicator
                ).exists()
                for indicator in indicators
            ):

                return candidate

        return None


    def detect_framework(
        self,
        project
    ):

        if (
            project
            /
            "capacitor.config.json"
        ).exists():

            return "capacitor"

        if (
            project
            /
            "capacitor.config.ts"
        ).exists():

            return "capacitor"

        if (
            project
            /
            "package.json"
        ).exists():

            return "node"

        return "generic"


    def inspect(
        self,
        path
    ):

        project = (
            Path(path)
            .expanduser()
            .resolve()
        )

        checks = []

        project_ok = (
            project.exists()
            and
            project.is_dir()
        )

        self._check(
            checks,
            "project",
            project_ok,
            project,
            required=True,
            message=(
                None
                if project_ok
                else "Project directory does not exist"
            ),
        )

        report = {
            "schema":
            "anbe.preflight.v1",

            "created":
            datetime.now().isoformat(),

            "project":
            str(project),

            "framework":
            None,

            "android_root":
            None,

            "checks":
            checks,

            "errors":
            [],

            "warnings":
            [],

            "ready":
            False,
        }

        if not project_ok:

            report["errors"].append(
                "Project directory does not exist"
            )

            return report

        framework = self.detect_framework(
            project
        )

        report["framework"] = (
            framework
        )

        android_root = (
            self.detect_android_root(
                project
            )
        )

        if android_root:

            try:

                android_value = str(
                    android_root.relative_to(
                        project
                    )
                )

                if android_value == ".":
                    android_value = "."

            except ValueError:

                android_value = str(
                    android_root
                )

        else:

            android_value = None

        report[
            "android_root"
        ] = android_value

        self._check(
            checks,
            "android_project",
            android_root is not None,
            android_value,
            required=True,
            message=(
                None
                if android_root
                else "Android project not detected"
            ),
        )

        node = self.which(
            "node"
        )

        node_required = (
            framework
            in (
                "capacitor",
                "node",
            )
        )

        self._check(
            checks,
            "node",
            node is not None,
            node,
            required=node_required,
        )

        package_manager_info = (
            self.package_manager_resolver
            .detect(
                project
            )
            if node_required
            else {
                "name":
                "npm",

                "version":
                None,

                "source":
                "default",
            }
        )

        package_manager = (
            package_manager_info[
                "name"
            ]
        )

        package_manager_version = (
            package_manager_info.get(
                "version"
            )
        )

        package_manager_path = (
            self.which(
                package_manager
            )
            if node_required
            else None
        )

        package_manager_message = None

        if (
            node_required
            and
            package_manager_path is None
        ):

            if package_manager == "pnpm":

                corepack = self.which(
                    "corepack"
                )

                if (
                    corepack
                    and
                    package_manager_version
                ):

                    package_manager_message = (
                        "Project requires pnpm "
                        +
                        package_manager_version
                        +
                        ". Try: corepack enable && "
                        "corepack prepare pnpm@"
                        +
                        package_manager_version
                        +
                        " --activate"
                    )

                elif corepack:

                    package_manager_message = (
                        "Project requires pnpm. "
                        "Try enabling it with Corepack."
                    )

                else:

                    package_manager_message = (
                        "Project requires pnpm but "
                        "pnpm is not installed."
                    )

            elif package_manager == "yarn":

                corepack = self.which(
                    "corepack"
                )

                if corepack:

                    package_manager_message = (
                        "Project requires yarn. "
                        "Try enabling it with Corepack."
                    )

                else:

                    package_manager_message = (
                        "Project requires yarn but "
                        "yarn is not installed."
                    )

            elif package_manager == "bun":

                package_manager_message = (
                    "Project requires bun but "
                    "bun is not installed."
                )

            else:

                package_manager_message = (
                    "Project requires npm but "
                    "npm is not installed."
                )

        self._check(
            checks,
            "package_manager",
            (
                package_manager_path is not None
                if node_required
                else True
            ),
            (
                (
                    package_manager
                    +
                    (
                        "@"
                        +
                        package_manager_version
                        if package_manager_version
                        else ""
                    )
                    +
                    (
                        " -> "
                        +
                        str(package_manager_path)
                        if package_manager_path
                        else ""
                    )
                )
                if node_required
                else None
            ),
            required=node_required,
            message=package_manager_message,
        )

        if (
            framework
            ==
            "capacitor"
        ):

            if package_manager == "npm":

                capacitor_runner = (
                    self.which(
                        "npx"
                    )
                )

                capacitor_runner_name = (
                    "npx"
                )

            elif package_manager == "bun":

                capacitor_runner = (
                    self.which(
                        "bunx"
                    )
                    or
                    package_manager_path
                )

                capacitor_runner_name = (
                    "bunx"
                )

            else:

                capacitor_runner = (
                    package_manager_path
                )

                capacitor_runner_name = (
                    package_manager
                )

            self._check(
                checks,
                "capacitor_runner",
                capacitor_runner is not None,
                (
                    capacitor_runner_name
                    +
                    (
                        " -> "
                        +
                        str(
                            capacitor_runner
                        )
                        if capacitor_runner
                        else ""
                    )
                ),
                required=True,
            )

        if android_root:

            gradlew = (
                android_root
                /
                "gradlew"
            )

            self._check(
                checks,
                "gradlew",
                (
                    gradlew.exists()
                    and
                    gradlew.is_file()
                ),
                gradlew,
                required=True,
            )

            try:

                gradle_version = (
                    self.java_resolver
                    .gradle_version(
                        android_root
                    )
                )

            except Exception:

                gradle_version = None

            self._check(
                checks,
                "gradle_version",
                gradle_version is not None,
                gradle_version,
                required=False,
            )

            try:

                required_java = (
                    self.java_resolver
                    .required_java(
                        android_root
                    )
                )

            except Exception:

                required_java = None

            try:

                java_home = (
                    self.java_resolver
                    .resolve(
                        android_root
                    )
                )

            except Exception:

                java_home = None

            self._check(
                checks,
                "java",
                java_home is not None,
                java_home,
                required=True,
                message=(
                    (
                        "Required Java: "
                        +
                        str(required_java)
                    )
                    if required_java
                    else None
                ),
            )

        try:

            tools = (
                self.android_toolchain
                .resolve()
            )

        except Exception:

            tools = {}

        aapt2 = tools.get(
            "aapt2"
        )

        self._check(
            checks,
            "aapt2",
            aapt2 is not None,
            aapt2,
            required=True,
        )

        for tool in (
            "aidl",
            "zipalign",
            "apksigner",
        ):

            value = tools.get(
                tool
            )

            self._check(
                checks,
                tool,
                value is not None,
                value,
                required=False,
            )

        sdk = (
            os.environ.get(
                "ANDROID_SDK_ROOT"
            )
            or
            os.environ.get(
                "ANDROID_HOME"
            )
        )

        sdk_path = (
            Path(sdk)
            if sdk
            else None
        )

        self._check(
            checks,
            "android_sdk",
            (
                sdk_path is not None
                and
                sdk_path.exists()
            ),
            sdk_path,
            required=False,
            message=(
                "ANDROID_SDK_ROOT/ANDROID_HOME not detected"
                if sdk_path is None
                else None
            ),
        )

        for item in checks:

            if (
                item["status"]
                ==
                "FAIL"
            ):

                report[
                    "errors"
                ].append(
                    item["name"]
                )

            elif (
                item["status"]
                ==
                "WARN"
            ):

                report[
                    "warnings"
                ].append(
                    item["name"]
                )

        report["ready"] = (
            len(
                report["errors"]
            )
            ==
            0
        )

        return report


    def save(
        self,
        report,
        folder="reports"
    ):

        out = Path(
            folder
        )

        out.mkdir(
            parents=True,
            exist_ok=True
        )

        stamp = (
            datetime.now()
            .strftime(
                "%Y%m%d-%H%M%S"
            )
        )

        path = (
            out
            /
            (
                "preflight-"
                +
                stamp
                +
                ".json"
            )
        )

        path.write_text(
            json.dumps(
                report,
                indent=2,
                ensure_ascii=False,
            )
            +
            "\n"
        )

        return path


    def print_report(
        self,
        report
    ):

        print()
        print(
            "ANBE PREFLIGHT"
        )
        print(
            "=" * 48
        )

        print(
            "Project:",
            report["project"]
        )

        print(
            "Framework:",
            report["framework"]
        )

        print(
            "Android root:",
            report["android_root"]
        )

        print()

        for item in report["checks"]:

            status = item[
                "status"
            ]

            name = item[
                "name"
            ]

            value = item.get(
                "value"
            )

            line = (
                f"[{status}] "
                f"{name}"
            )

            if value:

                line += (
                    ": "
                    +
                    str(value)
                )

            print(
                line
            )

            message = item.get(
                "message"
            )

            if message:

                print(
                    "       ",
                    message
                )

        print()
        print(
            "READY TO BUILD:",
            (
                "YES"
                if report["ready"]
                else "NO"
            )
        )

        return report


    def run(
        self,
        path,
        save=True,
    ):

        report = self.inspect(
            path
        )

        self.print_report(
            report
        )

        if save:

            output = self.save(
                report
            )

            print(
                "Report:",
                output
            )

        return report
