#!/usr/bin/env python3

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.native_dependency_compatibility import (
    NativeDependencyCompatibility,
)


class FakeHost:

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


class NonTermuxHost:

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


def make_project(
    root,
    with_assets=True,
):

    root = Path(
        root
    )

    dev = {
        "vite":
        "^7.0.0"
    }

    if with_assets:

        dev[
            "@capacitor/assets"
        ] = "^3.0.5"

    (
        root
        /
        "package.json"
    ).write_text(
        json.dumps({
            "devDependencies":
            dev
        })
        +
        "\n"
    )

    (
        root
        /
        "pnpm-workspace.yaml"
    ).write_text(
        "onlyBuiltDependencies:\n"
        "  - '@tailwindcss/oxide'\n"
        "  - esbuild\n"
        "  - sharp\n"
        "\n"
        "packages:\n"
        "  - .\n"
    )

    return root


def test_sharp_build_disabled_on_termux_android_arm64():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        compat = (
            NativeDependencyCompatibility(
                host_environment=FakeHost()
            )
        )

        result = compat.repair(
            root
        )

        assert result[
            "changed"
        ]

        text = (
            root
            /
            "pnpm-workspace.yaml"
        ).read_text()

        assert (
            "  - sharp"
            not in text
        )

        assert (
            "  - esbuild"
            in text
        )

        assert (
            "  - '@tailwindcss/oxide'"
            in text
        )


def test_repair_idempotent():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        compat = (
            NativeDependencyCompatibility(
                host_environment=FakeHost()
            )
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


def test_non_termux_host_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        compat = (
            NativeDependencyCompatibility(
                host_environment=NonTermuxHost()
            )
        )

        result = compat.repair(
            root
        )

        assert (
            result[
                "changed"
            ]
            is False
        )

        text = (
            root
            /
            "pnpm-workspace.yaml"
        ).read_text()

        assert (
            "  - sharp"
            in text
        )


def test_without_capacitor_assets_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            with_assets=False,
        )

        compat = (
            NativeDependencyCompatibility(
                host_environment=FakeHost()
            )
        )

        result = compat.repair(
            root
        )

        assert (
            result[
                "changed"
            ]
            is False
        )
