#!/usr/bin/env python3

import re
from pathlib import Path


class GradleCompatibility:

    def wrapper_file(
        self,
        android_root,
    ):

        return (
            Path(android_root)
            /
            "gradle"
            /
            "wrapper"
            /
            "gradle-wrapper.properties"
        )


    def version_tuple(
        self,
        value,
    ):

        if not value:

            return ()

        match = re.match(
            r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?",
            str(value),
        )

        if not match:

            return ()

        return tuple(
            int(part or 0)
            for part in match.groups()
        )


    def gradle_version(
        self,
        android_root,
    ):

        wrapper = self.wrapper_file(
            android_root
        )

        if not wrapper.exists():

            return None

        text = wrapper.read_text(
            errors="ignore"
        )

        match = re.search(
            r"gradle-([0-9]+(?:\.[0-9]+){1,2})-",
            text,
        )

        if not match:

            return None

        return match.group(1)


    def distribution_url(
        self,
        android_root,
    ):

        wrapper = self.wrapper_file(
            android_root
        )

        if not wrapper.exists():

            return None

        text = wrapper.read_text(
            errors="ignore"
        )

        match = re.search(
            r"^distributionUrl=(.+)$",
            text,
            re.MULTILINE,
        )

        if not match:

            return None

        return match.group(1).strip()


    def agp_version(
        self,
        android_root,
    ):

        root = Path(
            android_root
        )

        candidates = []

        for name in (
            "build.gradle",
            "build.gradle.kts",
            "settings.gradle",
            "settings.gradle.kts",
        ):

            path = (
                root
                /
                name
            )

            if path.exists():

                candidates.append(
                    path
                )

        for path in root.rglob(
            "*.gradle"
        ):

            if path not in candidates:

                candidates.append(
                    path
                )

        for path in root.rglob(
            "*.gradle.kts"
        ):

            if path not in candidates:

                candidates.append(
                    path
                )

        patterns = (
            re.compile(
                r"com\.android\.tools\.build:gradle:"
                r"([0-9]+(?:\.[0-9]+){1,2})"
            ),
            re.compile(
                r"""id\s*\(?\s*["']com\.android\.(?:application|library)["']\s*\)?\s*version\s*["']([0-9]+(?:\.[0-9]+){1,2})["']"""
            ),
        )

        for path in candidates:

            try:

                text = path.read_text(
                    errors="ignore"
                )

            except Exception:

                continue

            for pattern in patterns:

                match = pattern.search(
                    text
                )

                if match:

                    return match.group(1)

        return None


    def required_gradle(
        self,
        agp_version,
    ):

        version = self.version_tuple(
            agp_version
        )

        if not version:

            return None

        major = version[0]

        if major >= 8:

            return "8.0"

        return None


    def invalid_local_url(
        self,
        url,
    ):

        if not url:

            return False

        plain = (
            str(url)
            .replace(
                "\\:",
                ":"
            )
        )

        return (
            "://localhost"
            in plain
            or
            "://127.0.0.1"
            in plain
        )


    def official_url(
        self,
        version,
        distribution="all",
    ):

        return (
            "https\\://services.gradle.org/"
            "distributions/"
            "gradle-"
            +
            str(version)
            +
            "-"
            +
            str(distribution)
            +
            ".zip"
        )


    def distribution_type(
        self,
        url,
    ):

        if (
            url
            and
            "-bin.zip"
            in url
        ):

            return "bin"

        return "all"


    def replace_distribution(
        self,
        android_root,
        version,
    ):

        wrapper = self.wrapper_file(
            android_root
        )

        if not wrapper.exists():

            return False

        text = wrapper.read_text(
            errors="ignore"
        )

        current = self.distribution_url(
            android_root
        )

        distribution = self.distribution_type(
            current
        )

        replacement = (
            "distributionUrl="
            +
            self.official_url(
                version,
                distribution=distribution,
            )
        )

        updated, count = re.subn(
            r"^distributionUrl=.+$",
            replacement,
            text,
            count=1,
            flags=re.MULTILINE,
        )

        if count != 1:

            return False

        wrapper.write_text(
            updated
        )

        return True


    def inspect(
        self,
        android_root,
    ):

        gradle = self.gradle_version(
            android_root
        )

        agp = self.agp_version(
            android_root
        )

        url = self.distribution_url(
            android_root
        )

        required = self.required_gradle(
            agp
        )

        too_old = False

        if (
            gradle
            and
            required
        ):

            too_old = (
                self.version_tuple(
                    gradle
                )
                <
                self.version_tuple(
                    required
                )
            )

        return {
            "gradle_version":
            gradle,

            "agp_version":
            agp,

            "required_gradle":
            required,

            "distribution_url":
            url,

            "local_distribution_url":
            self.invalid_local_url(
                url
            ),

            "gradle_too_old":
            too_old,
        }


    def repair(
        self,
        android_root,
    ):

        before = self.inspect(
            android_root
        )

        actions = []

        target_version = (
            before[
                "gradle_version"
            ]
        )

        if (
            before[
                "gradle_too_old"
            ]
            and
            before[
                "required_gradle"
            ]
        ):

            target_version = (
                before[
                    "required_gradle"
                ]
            )

            if self.replace_distribution(
                android_root,
                target_version,
            ):

                actions.append({
                    "type":
                    "gradle_version",

                    "from":
                    before[
                        "gradle_version"
                    ],

                    "to":
                    target_version,
                })

        elif (
            before[
                "local_distribution_url"
            ]
            and
            target_version
        ):

            if self.replace_distribution(
                android_root,
                target_version,
            ):

                actions.append({
                    "type":
                    "distribution_url",

                    "from":
                    before[
                        "distribution_url"
                    ],

                    "to":
                    self.distribution_url(
                        android_root
                    ),
                })

        after = self.inspect(
            android_root
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
