#!/usr/bin/env python3

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.package_manager import PackageManagerResolver


def make_project(
    root,
    angular,
    webpack,
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
            "scripts": {
                "build":
                "ng build"
            },

            "devDependencies": {
                "@angular-devkit/build-angular":
                angular
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
            "lockfileVersion":
            3,

            "packages": {
                "node_modules/webpack": {
                    "version":
                    webpack
                }
            }
        })
        +
        "\n"
    )

    return root


def test_angular12_webpack5_uses_legacy_openssl():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            "~12.1.1",
            "5.44.0",
        )

        command = (
            PackageManagerResolver()
            .commands(
                root
            )[
                "build"
            ]
        )

        assert (
            command
            ==
            "NODE_OPTIONS=--openssl-legacy-provider "
            "npm run build"
        )


def test_angular13_not_modified():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            "13.3.0",
            "5.70.0",
        )

        command = (
            PackageManagerResolver()
            .commands(
                root
            )[
                "build"
            ]
        )

        assert (
            command
            ==
            "npm run build"
        )


def test_non_angular_not_modified():

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
                    "vite build"
                }
            })
            +
            "\n"
        )

        command = (
            PackageManagerResolver()
            .commands(
                root
            )[
                "build"
            ]
        )

        assert (
            command
            ==
            "npm run build"
        )
