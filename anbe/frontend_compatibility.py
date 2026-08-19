#!/usr/bin/env python3

import json
import re
from pathlib import Path


class FrontendCompatibility:

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

        should_repair = (
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

        if not should_repair:

            return {
                "before":
                before,

                "after":
                before,

                "actions":
                [],

                "changed":
                False,
            }

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
