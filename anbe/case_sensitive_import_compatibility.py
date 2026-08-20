#!/usr/bin/env python3

import re
from pathlib import Path


class CaseSensitiveImportCompatibility:

    SOURCE_SUFFIXES = {
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".mjs",
        ".cjs",
    }

    RESOLVE_SUFFIXES = (
        "",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".mjs",
        ".cjs",
        ".json",
    )


    def source_files(
        self,
        project,
    ):

        project = Path(
            project
        )

        roots = []

        for name in (
            "src",
            "app",
            "pages",
        ):

            root = (
                project
                /
                name
            )

            if root.exists():

                roots.append(
                    root
                )

        files = []

        for root in roots:

            for path in root.rglob(
                "*"
            ):

                if (
                    path.is_file()
                    and
                    path.suffix
                    in self.SOURCE_SUFFIXES
                ):

                    files.append(
                        path
                    )

        return files


    def import_specifiers(
        self,
        text,
    ):

        patterns = (
            re.compile(
                r"""from\s+["']([^"']+)["']"""
            ),
            re.compile(
                r"""import\s*\(\s*["']([^"']+)["']\s*\)"""
            ),
            re.compile(
                r"""require\s*\(\s*["']([^"']+)["']\s*\)"""
            ),
        )

        found = []

        for pattern in patterns:

            for match in pattern.finditer(
                text
            ):

                specifier = (
                    match.group(1)
                )

                if specifier.startswith(
                    "."
                ):

                    found.append(
                        specifier
                    )

        return found


    def exact_exists(
        self,
        source,
        specifier,
    ):

        base = (
            source.parent
            /
            specifier
        )

        if base.exists():

            return True

        for suffix in self.RESOLVE_SUFFIXES:

            candidate = Path(
                str(base)
                +
                suffix
            )

            if candidate.exists():

                return True

        if base.is_dir():

            for suffix in self.RESOLVE_SUFFIXES[1:]:

                candidate = (
                    base
                    /
                    (
                        "index"
                        +
                        suffix
                    )
                )

                if candidate.exists():

                    return True

        return False


    def resolve_case_match(
        self,
        source,
        specifier,
    ):

        base = (
            source.parent
            /
            specifier
        )

        parent = base.parent

        if not parent.exists():

            return None

        target_name = (
            base.name
        )

        matches = []

        for item in parent.iterdir():

            if (
                item.name.lower()
                ==
                target_name.lower()
            ):

                matches.append(
                    item
                )

        if len(matches) == 1:

            return matches[0]

        for suffix in self.RESOLVE_SUFFIXES[1:]:

            target = (
                target_name
                +
                suffix
            )

            matches = [
                item
                for item in parent.iterdir()
                if (
                    item.is_file()
                    and
                    item.name.lower()
                    ==
                    target.lower()
                )
            ]

            if len(matches) == 1:

                return matches[0]

        return None


    def corrected_specifier(
        self,
        source,
        specifier,
        match,
    ):

        original = Path(
            specifier
        )

        corrected = (
            original.parent
            /
            match.name
        )

        value = str(
            corrected
        )

        if not value.startswith(
            "."
        ):

            value = (
                "./"
                +
                value
            )

        for suffix in self.RESOLVE_SUFFIXES[1:]:

            if (
                specifier.lower()
                .endswith(
                    suffix
                )
            ):

                return value

            if (
                match.name.lower()
                .endswith(
                    suffix
                )
                and
                not specifier.lower()
                .endswith(
                    suffix
                )
            ):

                value = value[
                    :
                    -len(
                        suffix
                    )
                ]

                return value

        return value


    def inspect_file(
        self,
        path,
    ):

        try:

            text = path.read_text(
                errors="ignore"
            )

        except Exception:

            return []

        repairs = []

        for specifier in self.import_specifiers(
            text
        ):

            if self.exact_exists(
                path,
                specifier,
            ):

                continue

            match = self.resolve_case_match(
                path,
                specifier,
            )

            if not match:

                continue

            corrected = self.corrected_specifier(
                path,
                specifier,
                match,
            )

            if corrected == specifier:

                continue

            repairs.append({
                "from":
                specifier,

                "to":
                corrected,
            })

        return repairs


    def repair(
        self,
        project,
    ):

        actions = []

        for path in self.source_files(
            project
        ):

            repairs = self.inspect_file(
                path
            )

            if not repairs:

                continue

            text = path.read_text(
                errors="ignore"
            )

            original = text

            for item in repairs:

                text = text.replace(
                    item[
                        "from"
                    ],
                    item[
                        "to"
                    ],
                )

                actions.append({
                    "type":
                    "case_sensitive_import",

                    "file":
                    str(path),

                    "from":
                    item[
                        "from"
                    ],

                    "to":
                    item[
                        "to"
                    ],
                })

            if text != original:

                path.write_text(
                    text
                )

        return {
            "actions":
            actions,

            "changed":
            bool(actions),
        }
