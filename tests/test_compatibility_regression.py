#!/usr/bin/env python3

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.repair import RepairEngine


class FakeContext:

    def __init__(self, path):

        self.path = str(path)
        self.runtime = {}
        self.aapt2 = "/fake/runtime/aapt2"
        self.messages = []


    def log(self, message):

        self.messages.append(
            str(message)
        )


    def warn(self, message):

        self.messages.append(
            str(message)
        )


def make_broken_project(root):

    root = Path(root)

    (
        root
        /
        "package.json"
    ).write_text(
        json.dumps(
            {
                "name": "compat-regression",

                "scripts": {
                    "build": "vite build"
                },

                "devDependencies": {
                    "@sveltejs/adapter-auto": "^3.0.0",
                    "@sveltejs/kit": "^2.0.0",
                    "vite": "^5.0.3"
                },

                "dependencies": {
                    "@capacitor/core": "^5.7.4"
                }
            },
            indent=2,
        )
        +
        "\n"
    )

    (
        root
        /
        "svelte.config.js"
    ).write_text(
        "import adapter from "
        "'@sveltejs/adapter-auto';\n"
        "\n"
        "const config = {\n"
        "  kit: {\n"
        "    adapter: adapter()\n"
        "  }\n"
        "};\n"
        "\n"
        "export default config;\n"
    )

    (
        root
        /
        "capacitor.config.ts"
    ).write_text(
        "const config = {\n"
        "  appId: 'example.compat',\n"
        "  appName: 'Compatibility Test',\n"
        "  webDir: 'dist'\n"
        "};\n"
        "\n"
        "export default config;\n"
    )

    android = root / "android"
    android.mkdir()

    (
        android
        /
        "gradlew"
    ).write_text(
        "#!/bin/sh\n"
    )

    (
        android
        /
        "build.gradle"
    ).write_text(
        "buildscript {\n"
        "  dependencies {\n"
        "    classpath "
        "\"com.android.tools.build:gradle:8.0.2\"\n"
        "  }\n"
        "}\n"
    )

    wrapper = (
        android
        /
        "gradle"
        /
        "wrapper"
    )

    wrapper.mkdir(
        parents=True
    )

    (
        wrapper
        /
        "gradle-wrapper.properties"
    ).write_text(
        "distributionBase=GRADLE_USER_HOME\n"
        "distributionPath=wrapper/dists\n"
        "distributionUrl="
        "http\\://localhost:8000/"
        "gradle-7.3.2-all.zip\n"
        "zipStoreBase=GRADLE_USER_HOME\n"
        "zipStorePath=wrapper/dists\n"
    )

    return root


def test_compatibility_repair_flow():

    with TemporaryDirectory() as tmp:

        root = make_broken_project(
            tmp
        )

        ctx = FakeContext(
            root
        )

        RepairEngine().run(
            ctx
        )

        package = json.loads(
            (
                root
                /
                "package.json"
            ).read_text()
        )

        dev = package[
            "devDependencies"
        ]

        assert (
            "@sveltejs/adapter-auto"
            not in dev
        )

        assert (
            dev[
                "@sveltejs/adapter-static"
            ]
            ==
            "^3.0.0"
        )

        svelte = (
            root
            /
            "svelte.config.js"
        ).read_text()

        assert (
            "@sveltejs/adapter-static"
            in svelte
        )

        assert (
            "fallback: 'index.html'"
            in svelte
        )

        capacitor = (
            root
            /
            "capacitor.config.ts"
        ).read_text()

        assert (
            "webDir: 'build'"
            in capacitor
        )

        wrapper = (
            root
            /
            "android"
            /
            "gradle"
            /
            "wrapper"
            /
            "gradle-wrapper.properties"
        ).read_text()

        assert (
            "localhost"
            not in wrapper
        )

        assert (
            "services.gradle.org"
            in wrapper
        )

        assert (
            "gradle-8.0-all.zip"
            in wrapper
        )

        frontend = (
            ctx.runtime[
                "frontend_compatibility"
            ]
        )

        gradle = (
            ctx.runtime[
                "gradle_compatibility"
            ]
        )

        assert frontend[
            "changed"
        ]

        assert gradle[
            "changed"
        ]

        frontend_types = {
            action["type"]
            for action
            in frontend["actions"]
        }

        assert (
            "package_dependency"
            in frontend_types
        )

        assert (
            "svelte_adapter"
            in frontend_types
        )

        assert (
            "capacitor_web_dir"
            in frontend_types
        )

        gradle_types = {
            action["type"]
            for action
            in gradle["actions"]
        }

        assert (
            "gradle_version"
            in gradle_types
        )

        assert any(
            "SvelteKit static build enabled"
            in message
            for message in ctx.messages
        )

        assert any(
            "Gradle wrapper upgraded"
            in message
            for message in ctx.messages
        )


def test_compatibility_repair_flow_idempotent():

    with TemporaryDirectory() as tmp:

        root = make_broken_project(
            tmp
        )

        first = FakeContext(
            root
        )

        RepairEngine().run(
            first
        )

        second = FakeContext(
            root
        )

        RepairEngine().run(
            second
        )

        assert (
            second.runtime[
                "frontend_compatibility"
            ][
                "changed"
            ]
            is False
        )

        assert (
            second.runtime[
                "gradle_compatibility"
            ][
                "changed"
            ]
            is False
        )

        wrapper = (
            root
            /
            "android"
            /
            "gradle"
            /
            "wrapper"
            /
            "gradle-wrapper.properties"
        ).read_text()

        assert (
            wrapper.count(
                "distributionUrl="
            )
            ==
            1
        )

        assert (
            wrapper.count(
                "gradle-8.0-all.zip"
            )
            ==
            1
        )
