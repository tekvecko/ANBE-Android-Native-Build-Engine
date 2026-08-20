#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory
import json

from anbe.package_manager import PackageManagerResolver


class TermuxHost:

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


def make_project(
    root,
    manager=None,
):

    root = Path(
        root
    )

    package = {
        "scripts": {
            "build":
            "echo build"
        }
    }

    if manager:

        package[
            "packageManager"
        ] = manager

    (
        root
        /
        "package.json"
    ).write_text(
        json.dumps(
            package
        )
        +
        "\n"
    )

    return root


def test_npm_termux_install_command():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        resolver = PackageManagerResolver(
            host_environment=TermuxHost()
        )

        command = resolver.commands(
            root
        )[
            "install"
        ]

        assert (
            command
            ==
            "npm install"
        )


def test_npm_linux_install_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        resolver = PackageManagerResolver(
            host_environment=LinuxHost()
        )

        assert (
            resolver.commands(
                root
            )[
                "install"
            ]
            ==
            "npm install"
        )


def test_pnpm_termux_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            "pnpm@10.28.0",
        )

        resolver = PackageManagerResolver(
            host_environment=TermuxHost()
        )

        assert (
            resolver.commands(
                root
            )[
                "install"
            ]
            ==
            "pnpm install"
        )


def test_yarn_termux_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            "yarn@1.22.22",
        )

        resolver = PackageManagerResolver(
            host_environment=TermuxHost()
        )

        assert (
            resolver.commands(
                root
            )[
                "install"
            ]
            ==
            "yarn install"
        )

def test_plain_npm_termux_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        resolver = PackageManagerResolver(
            host_environment=TermuxHost()
        )

        assert (
            resolver.commands(
                root
            )[
                "install"
            ]
            ==
            "npm install"
        )


def test_puppeteer_termux_uses_safe_install():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        (
            root
            /
            "package.json"
        ).write_text(
            json.dumps({
                "scripts": {
                    "build":
                    "ng build"
                },

                "devDependencies": {
                    "puppeteer":
                    "24.37.5"
                }
            })
            +
            "\n"
        )

        (
            root
            /
            "package-lock.json"
        ).write_text(
            json.dumps({
                "name":
                "test",

                "lockfileVersion":
                3,

                "requires":
                True,

                "packages":
                {}
            })
            +
            "\n"
        )

        resolver = PackageManagerResolver(
            host_environment=TermuxHost()
        )

        assert (
            resolver.commands(
                root
            )[
                "install"
            ]
            ==
            "PUPPETEER_SKIP_DOWNLOAD=true "
            "npm ci --omit=optional"
        )
