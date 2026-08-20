#!/usr/bin/env python3

from pathlib import Path
import os
import re


class JavaResolver:

    def __init__(self):

        self.termux_jvm = Path(
            "/data/data/com.termux/files/usr/lib/jvm"
        )


    def gradle_version(self, root):

        wrapper = (
            Path(root)
            / "gradle"
            / "wrapper"
            / "gradle-wrapper.properties"
        )

        if not wrapper.exists():
            return None

        text = wrapper.read_text(
            errors="ignore"
        )

        match = re.search(
            r"gradle-([0-9]+\.[0-9]+)",
            text
        )

        if match:
            return match.group(1)

        return None


    def project_java_version(self, root):

        root = Path(root)

        patterns = [
            re.compile(
                r"JavaVersion\.VERSION_(\d+)"
            ),
            re.compile(
                r"JavaLanguageVersion\.of\((\d+)\)"
            ),
            re.compile(
                r"languageVersion\s*=\s*JavaLanguageVersion\.of\((\d+)\)"
            ),
        ]

        files = []

        for pattern in (
            "*.gradle",
            "*.gradle.kts",
        ):
            files.extend(
                root.rglob(pattern)
            )

        versions = []

        for file in files:

            try:
                text = file.read_text(
                    errors="ignore"
                )
            except Exception:
                continue

            for pattern in patterns:

                for match in pattern.finditer(
                    text
                ):
                    try:
                        versions.append(
                            int(
                                match.group(1)
                            )
                        )
                    except Exception:
                        pass

        if versions:
            return max(versions)

        return None


    def required_java(
        self,
        root
    ):

        project_version = (
            self.project_java_version(
                root
            )
        )

        if project_version:
            return project_version

        gradle = self.gradle_version(
            root
        )

        if not gradle:
            return 17

        try:
            major = float(
                gradle
            )
        except Exception:
            return 17

        if major >= 8.5:
            return 21

        return 17


    def version_tuple(
        self,
        value,
    ):

        if not value:

            return ()

        parts = []

        for item in str(value).split(
            "."
        ):

            try:

                parts.append(
                    int(item)
                )

            except Exception:

                break

        return tuple(
            parts
        )


    def gradle_runtime_max_java(
        self,
        root,
    ):

        gradle = self.gradle_version(
            root
        )

        version = self.version_tuple(
            gradle
        )

        if not version:

            return None

        if version < (
            7,
            6,
        ):

            return 17

        if version < (
            8,
            5,
        ):

            return 21

        return None


    def runtime_java(
        self,
        root,
    ):

        required = self.required_java(
            root
        )

        maximum = self.gradle_runtime_max_java(
            root
        )

        candidates = []

        if maximum is not None:

            candidates.append(
                min(
                    required,
                    maximum,
                )
            )

            for version in (
                21,
                17,
                11,
            ):

                if (
                    version
                    <=
                    maximum
                    and
                    version
                    not in candidates
                ):

                    candidates.append(
                        version
                    )

        else:

            candidates.append(
                required
            )

            for version in (
                21,
                17,
                11,
            ):

                if version not in candidates:

                    candidates.append(
                        version
                    )

        for version in candidates:

            java = self.find_java(
                version
            )

            if java:

                return str(
                    java
                )

        return None


    def find_java(
        self,
        version
    ):

        candidates = [
            f"java-{version}-openjdk",
            f"java-{version}",
        ]

        for candidate in candidates:

            path = (
                self.termux_jvm
                /
                candidate
            )

            if path.exists():
                return path

        return None


    def resolve(
        self,
        root
    ):

        root = Path(
            root
        )

        runtime = self.runtime_java(
            root
        )

        if runtime:

            return runtime

        current = os.environ.get(
            "JAVA_HOME"
        )

        if current:

            maximum = self.gradle_runtime_max_java(
                root
            )

            if maximum is None:

                return current

            match = re.search(
                r"java-(\\d+)",
                current,
            )

            if match:

                try:

                    version = int(
                        match.group(1)
                    )

                except Exception:

                    version = None

                if (
                    version is not None
                    and
                    version
                    <=
                    maximum
                ):

                    return current

        return None
