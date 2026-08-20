#!/usr/bin/env python3

import json
import re
from pathlib import Path

from .host_environment import HostEnvironment


class FrontendCompatibility:

    def __init__(
        self,
        host_environment=None,
    ):

        self.host_environment = (
            host_environment
            or
            HostEnvironment()
        )


    def package_file(
        self,
        project,
    ):

        return (
            Path(project)
            /
            "package.json"
        )


    def svelte_config(
        self,
        project,
    ):

        project = Path(
            project
        )

        for name in (
            "svelte.config.js",
            "svelte.config.mjs",
        ):

            path = (
                project
                /
                name
            )

            if path.exists():

                return path

        return None


    def capacitor_config(
        self,
        project,
    ):

        project = Path(
            project
        )

        for name in (
            "capacitor.config.ts",
            "capacitor.config.js",
            "capacitor.config.json",
        ):

            path = (
                project
                /
                name
            )

            if path.exists():

                return path

        return None


    def package(
        self,
        project,
    ):

        path = self.package_file(
            project
        )

        if not path.exists():

            return {}

        try:

            return json.loads(
                path.read_text()
            )

        except Exception:

            return {}


    def is_sveltekit(
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
            "@sveltejs/kit"
            in dependencies
        )


    def uses_adapter_auto(
        self,
        project,
    ):

        package = self.package(
            project
        )

        dev = package.get(
            "devDependencies",
            {}
        )

        config = self.svelte_config(
            project
        )

        if not config:

            return False

        try:

            text = config.read_text(
                errors="ignore"
            )

        except Exception:

            return False

        return (
            "@sveltejs/adapter-auto"
            in dev
            and
            "@sveltejs/adapter-auto"
            in text
        )


    def capacitor_web_dir(
        self,
        project,
    ):

        config = self.capacitor_config(
            project
        )

        if not config:

            return None

        text = config.read_text(
            errors="ignore"
        )

        if (
            config.suffix
            ==
            ".json"
        ):

            try:

                data = json.loads(
                    text
                )

            except Exception:

                return None

            return data.get(
                "webDir"
            )

        match = re.search(
            r"""webDir\s*:\s*["']([^"']+)["']""",
            text,
        )

        if not match:

            return None

        return match.group(1)


    def next_version(
        self,
        project,
    ):

        package = self.package(
            project
        )

        for section in (
            "dependencies",
            "devDependencies",
        ):

            values = package.get(
                section,
                {}
            )

            version = values.get(
                "next"
            )

            if version:

                return str(
                    version
                )

        return None


    def next_major(
        self,
        project,
    ):

        version = self.next_version(
            project
        )

        if not version:

            return None

        match = re.search(
            r"(\d+)",
            version,
        )

        if not match:

            return None

        return int(
            match.group(1)
        )


    def next_config(
        self,
        project,
    ):

        project = Path(
            project
        )

        for name in (
            "next.config.js",
            "next.config.cjs",
            "next.config.mjs",
        ):

            path = (
                project
                /
                name
            )

            if path.exists():

                return path

        return None


    def next_static_export(
        self,
        project,
    ):

        path = self.next_config(
            project
        )

        if not path:

            return False

        try:

            text = path.read_text(
                errors="ignore"
            )

        except Exception:

            return False

        return (
            re.search(
                r"""output\s*:\s*["']export["']""",
                text,
            )
            is not None
        )


    def pin_next_version(
        self,
        project,
        version,
    ):

        path = self.package_file(
            project
        )

        package = self.package(
            project
        )

        changed = False

        for section in (
            "dependencies",
            "devDependencies",
        ):

            values = package.get(
                section
            )

            if not isinstance(
                values,
                dict
            ):

                continue

            if (
                "next"
                in values
            ):

                if (
                    values[
                        "next"
                    ]
                    !=
                    version
                ):

                    values[
                        "next"
                    ] = version

                    changed = True

                break

        if not changed:

            return False

        path.write_text(
            json.dumps(
                package,
                indent=2,
                ensure_ascii=False,
            )
            +
            "\n"
        )

        return True


    def next_layout_files(
        self,
        project,
    ):

        project = Path(
            project
        )

        files = []

        for root in (
            project / "app",
            project / "src" / "app",
        ):

            if not root.exists():

                continue

            files.extend(
                root.rglob(
                    "layout.tsx"
                )
            )

            files.extend(
                root.rglob(
                    "layout.ts"
                )
            )

        return files


    def remove_next14_viewport_type(
        self,
        project,
    ):

        changed_files = []

        for path in self.next_layout_files(
            project
        ):

            try:

                text = path.read_text(
                    errors="ignore"
                )

            except Exception:

                continue

            original = text

            text = re.sub(
                (
                    r"import\s+type\s*\{"
                    r"([^}]*)"
                    r"\}\s+from\s+"
                    r"([\"'])next\2;"
                ),
                self._remove_viewport_from_import,
                text,
                count=1,
            )

            text = re.sub(
                (
                    r"export\s+const\s+viewport"
                    r"\s*:\s*Viewport"
                    r"\s*="
                ),
                "export const viewport =",
                text,
            )

            if text != original:

                path.write_text(
                    text
                )

                changed_files.append(
                    str(path)
                )

        return changed_files


    def _remove_viewport_from_import(
        self,
        match,
    ):

        names = [
            item.strip()
            for item in match.group(1).split(
                ","
            )
            if item.strip()
        ]

        names = [
            item
            for item in names
            if item != "Viewport"
        ]

        quote = match.group(2)

        if not names:

            return ""

        return (
            "import type { "
            +
            ", ".join(
                names
            )
            +
            " } from "
            +
            quote
            +
            "next"
            +
            quote
            +
            ";"
        )


    def inspect(
        self,
        project,
    ):

        project = Path(
            project
        )

        return {
            "sveltekit":
            self.is_sveltekit(
                project
            ),

            "adapter_auto":
            self.uses_adapter_auto(
                project
            ),

            "capacitor":
            (
                self.capacitor_config(
                    project
                )
                is not None
            ),

            "web_dir":
            self.capacitor_web_dir(
                project
            ),

            "next_version":
            self.next_version(
                project
            ),

            "next_major":
            self.next_major(
                project
            ),

            "next_static_export":
            self.next_static_export(
                project
            ),

            "host":
            self.host_environment
            .inspect(),
        }


    def replace_adapter_dependency(
        self,
        project,
    ):

        path = self.package_file(
            project
        )

        package = self.package(
            project
        )

        dev = package.get(
            "devDependencies"
        )

        if not isinstance(
            dev,
            dict
        ):

            return False

        version = dev.get(
            "@sveltejs/adapter-auto"
        )

        if not version:

            return False

        if (
            "@sveltejs/adapter-static"
            not in dev
        ):

            new_dev = {}

            for key, value in dev.items():

                if (
                    key
                    ==
                    "@sveltejs/adapter-auto"
                ):

                    new_dev[
                        "@sveltejs/adapter-static"
                    ] = value

                else:

                    new_dev[
                        key
                    ] = value

            package[
                "devDependencies"
            ] = new_dev

        else:

            dev.pop(
                "@sveltejs/adapter-auto",
                None,
            )

        path.write_text(
            json.dumps(
                package,
                indent=2,
                ensure_ascii=False,
            )
            +
            "\n"
        )

        return True


    def replace_svelte_adapter(
        self,
        project,
    ):

        path = self.svelte_config(
            project
        )

        if not path:

            return False

        text = path.read_text(
            errors="ignore"
        )

        original = text

        text = text.replace(
            "@sveltejs/adapter-auto",
            "@sveltejs/adapter-static",
        )

        text = re.sub(
            r"adapter\s*:\s*adapter\(\s*\)",
            (
                "adapter: adapter({ "
                "fallback: 'index.html' "
                "})"
            ),
            text,
            count=1,
        )

        if text == original:

            return False

        path.write_text(
            text
        )

        return True


    def set_capacitor_web_dir(
        self,
        project,
        web_dir,
    ):

        path = self.capacitor_config(
            project
        )

        if not path:

            return False

        text = path.read_text(
            errors="ignore"
        )

        if (
            path.suffix
            ==
            ".json"
        ):

            try:

                data = json.loads(
                    text
                )

            except Exception:

                return False

            if (
                data.get(
                    "webDir"
                )
                ==
                web_dir
            ):

                return False

            data[
                "webDir"
            ] = web_dir

            path.write_text(
                json.dumps(
                    data,
                    indent=2,
                    ensure_ascii=False,
                )
                +
                "\n"
            )

            return True

        updated, count = re.subn(
            (
                r"""webDir(\s*:\s*)"""
                r"""["'][^"']+["']"""
            ),
            (
                "webDir"
                +
                r"\1"
                +
                "'"
                +
                web_dir
                +
                "'"
            ),
            text,
            count=1,
        )

        if count != 1:

            return False

        if updated == text:

            return False

        path.write_text(
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

        # ---------------------------------------------
        # SvelteKit + Capacitor static compatibility
        # ---------------------------------------------

        svelte_repair = (
            before[
                "sveltekit"
            ]
            and
            before[
                "adapter_auto"
            ]
            and
            before[
                "capacitor"
            ]
        )

        if svelte_repair:

            if self.replace_adapter_dependency(
                project
            ):

                actions.append({
                    "type":
                    "package_dependency",

                    "from":
                    "@sveltejs/adapter-auto",

                    "to":
                    "@sveltejs/adapter-static",
                })

            if self.replace_svelte_adapter(
                project
            ):

                actions.append({
                    "type":
                    "svelte_adapter",

                    "from":
                    "adapter-auto",

                    "to":
                    "adapter-static",
                })

            if (
                before[
                    "web_dir"
                ]
                !=
                "build"
            ):

                if self.set_capacitor_web_dir(
                    project,
                    "build",
                ):

                    actions.append({
                        "type":
                        "capacitor_web_dir",

                        "from":
                        before[
                            "web_dir"
                        ],

                        "to":
                        "build",
                    })

        # ---------------------------------------------
        # Next 14 SWC compatibility on Termux ARM64
        # ---------------------------------------------

        host = before[
            "host"
        ]

        next_repair = (
            before[
                "next_major"
            ]
            ==
            14
            and
            before[
                "capacitor"
            ]
            and
            before[
                "next_static_export"
            ]
            and
            host[
                "termux"
            ]
            and
            host[
                "android"
            ]
            and
            host[
                "arm64"
            ]
        )

        if next_repair:

            if self.pin_next_version(
                project,
                "13.4.19",
            ):

                actions.append({
                    "type":
                    "next_version",

                    "from":
                    before[
                        "next_version"
                    ],

                    "to":
                    "13.4.19",

                    "reason":
                    "Next 14 native SWC unavailable on Termux Android ARM64",
                })

            viewport_files = (
                self.remove_next14_viewport_type(
                    project
                )
            )

            if viewport_files:

                actions.append({
                    "type":
                    "next_viewport_type",

                    "files":
                    viewport_files,
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
