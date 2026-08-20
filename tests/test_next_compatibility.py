#!/usr/bin/env python3

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.frontend_compatibility import FrontendCompatibility


class TermuxArm64Host:

    def inspect(self):

        return {
            "termux":
            True,

            "android":
            True,

            "arm64":
            True,

            "system":
            "linux",

            "machine":
            "aarch64",
        }


class LinuxHost:

    def inspect(self):

        return {
            "termux":
            False,

            "android":
            False,

            "arm64":
            True,

            "system":
            "linux",

            "machine":
            "aarch64",
        }


def make_next_project(
    root,
    version="14.2.32",
):

    root = Path(
        root
    )

    (
        root
        /
        "package.json"
    ).write_text(
        json.dumps({
            "dependencies": {
                "next":
                version,

                "react":
                "^18.2.0"
            },

            "scripts": {
                "build":
                "next build"
            }
        })
        +
        "\n"
    )

    (
        root
        /
        "next.config.js"
    ).write_text(
        "module.exports = {\n"
        "  output: 'export',\n"
        "  images: { unoptimized: true }\n"
        "};\n"
    )

    (
        root
        /
        "capacitor.config.ts"
    ).write_text(
        "const config = {\n"
        "  appId: 'example.next',\n"
        "  webDir: 'out'\n"
        "};\n"
        "\n"
        "export default config;\n"
    )

    app = (
        root
        /
        "app"
    )

    app.mkdir()

    (
        app
        /
        "layout.tsx"
    ).write_text(
        "import type { Metadata, Viewport } from 'next';\n"
        "\n"
        "export const metadata: Metadata = {\n"
        "  title: 'Test'\n"
        "};\n"
        "\n"
        "export const viewport: Viewport = {\n"
        "  initialScale: 1,\n"
        "  width: 'device-width',\n"
        "  viewportFit: 'cover'\n"
        "};\n"
    )

    return root


def test_next14_termux_repair():

    with TemporaryDirectory() as tmp:

        root = make_next_project(
            tmp
        )

        compat = FrontendCompatibility(
            host_environment=TermuxArm64Host()
        )

        result = compat.repair(
            root
        )

        assert result[
            "changed"
        ]

        package = json.loads(
            (
                root
                /
                "package.json"
            ).read_text()
        )

        assert (
            package[
                "dependencies"
            ][
                "next"
            ]
            ==
            "13.4.19"
        )

        layout = (
            root
            /
            "app"
            /
            "layout.tsx"
        ).read_text()

        assert (
            "Viewport"
            not in layout
        )

        assert (
            "Metadata"
            in layout
        )

        assert (
            "export const viewport = {"
            in layout
        )

        types = {
            action[
                "type"
            ]
            for action in result[
                "actions"
            ]
        }

        assert (
            "next_version"
            in types
        )

        assert (
            "next_viewport_type"
            in types
        )


def test_next_repair_idempotent():

    with TemporaryDirectory() as tmp:

        root = make_next_project(
            tmp
        )

        compat = FrontendCompatibility(
            host_environment=TermuxArm64Host()
        )

        first = compat.repair(
            root
        )

        second = compat.repair(
            root
        )

        assert first[
            "changed"
        ]

        assert (
            second[
                "changed"
            ]
            is False
        )


def test_next14_non_termux_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_next_project(
            tmp
        )

        result = (
            FrontendCompatibility(
                host_environment=LinuxHost()
            )
            .repair(
                root
            )
        )

        assert (
            result[
                "changed"
            ]
            is False
        )


def test_next13_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_next_project(
            tmp,
            version="13.4.19",
        )

        result = (
            FrontendCompatibility(
                host_environment=TermuxArm64Host()
            )
            .repair(
                root
            )
        )

        assert (
            result[
                "changed"
            ]
            is False
        )


def test_next14_without_static_export_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_next_project(
            tmp
        )

        (
            root
            /
            "next.config.js"
        ).write_text(
            "module.exports = {};\n"
        )

        result = (
            FrontendCompatibility(
                host_environment=TermuxArm64Host()
            )
            .repair(
                root
            )
        )

        assert (
            result[
                "changed"
            ]
            is False
        )
