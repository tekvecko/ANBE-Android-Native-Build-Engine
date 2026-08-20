#!/usr/bin/env python3

import re
from pathlib import Path


class AndroidDependencyCompatibility:

    TARGET_CORE_KTX = "1.17.0"


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


    def catalog_file(
        self,
        project,
    ):

        project = Path(
            project
        )

        candidates = (
            project
            /
            "gradle"
            /
            "libs.versions.toml",

            project
            /
            "android"
            /
            "gradle"
            /
            "libs.versions.toml",
        )

        for path in candidates:

            if path.exists():

                return path

        return None


    def value(
        self,
        text,
        key,
    ):

        match = re.search(
            (
                r"^"
                +
                re.escape(
                    key
                )
                +
                r'\s*=\s*"([^"]+)"'
            ),
            text,
            re.MULTILINE,
        )

        if not match:

            return None

        return match.group(1)


    def inspect(
        self,
        project,
    ):

        catalog = self.catalog_file(
            project
        )

        if not catalog:

            return {
                "catalog":
                None,

                "agp":
                None,

                "compile_sdk":
                None,

                "core_ktx":
                None,

                "needs_core_ktx_pin":
                False,
            }

        text = catalog.read_text(
            errors="ignore"
        )

        agp = self.value(
            text,
            "agp",
        )

        compile_sdk = self.value(
            text,
            "compile_sdk_version",
        )

        core_ktx = self.value(
            text,
            "core_ktx",
        )

        needs_pin = False

        agp_tuple = self.version_tuple(
            agp
        )

        core_tuple = self.version_tuple(
            core_ktx
        )

        try:

            compile_sdk_value = int(
                str(
                    compile_sdk
                )
            )

        except Exception:

            compile_sdk_value = None

        if (
            agp_tuple
            and
            agp_tuple[0]
            ==
            8
            and
            len(
                agp_tuple
            )
            >=
            2
            and
            agp_tuple[1]
            ==
            13
            and
            compile_sdk_value
            ==
            36
            and
            core_tuple
            >=
            self.version_tuple(
                "1.19.0"
            )
        ):

            needs_pin = True

        return {
            "catalog":
            str(
                catalog
            ),

            "agp":
            agp,

            "compile_sdk":
            compile_sdk,

            "core_ktx":
            core_ktx,

            "needs_core_ktx_pin":
            needs_pin,
        }


    def pin_core_ktx(
        self,
        project,
        version=None,
    ):

        version = (
            version
            or
            self.TARGET_CORE_KTX
        )

        catalog = self.catalog_file(
            project
        )

        if not catalog:

            return False

        text = catalog.read_text(
            errors="ignore"
        )

        updated, count = re.subn(
            r'^core_ktx\s*=\s*"[^"]+"',
            (
                'core_ktx = "'
                +
                version
                +
                '"'
            ),
            text,
            count=1,
            flags=re.MULTILINE,
        )

        if (
            count != 1
            or
            updated == text
        ):

            return False

        catalog.write_text(
            updated
        )

        return True


    def repair(
        self,
        project,
    ):

        before = self.inspect(
            project
        )

        actions = []

        if before[
            "needs_core_ktx_pin"
        ]:

            if self.pin_core_ktx(
                project
            ):

                actions.append({
                    "type":
                    "androidx_core_ktx_pin",

                    "from":
                    before[
                        "core_ktx"
                    ],

                    "to":
                    self.TARGET_CORE_KTX,

                    "agp":
                    before[
                        "agp"
                    ],

                    "compile_sdk":
                    before[
                        "compile_sdk"
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
