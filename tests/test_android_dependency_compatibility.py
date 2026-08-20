#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.android_dependency_compatibility import AndroidDependencyCompatibility


def make_project(
    root,
    agp="8.13.2",
    compile_sdk="36",
    core_ktx="1.19.0",
):

    root = Path(
        root
    )

    gradle = (
        root
        /
        "gradle"
    )

    gradle.mkdir(
        parents=True
    )

    (
        gradle
        /
        "libs.versions.toml"
    ).write_text(
        "[versions]\n"
        +
        'agp = "'
        +
        agp
        +
        '"\n'
        +
        'compile_sdk_version = "'
        +
        compile_sdk
        +
        '"\n'
        +
        'core_ktx = "'
        +
        core_ktx
        +
        '"\n'
        +
        "\n"
        +
        "[libraries]\n"
        +
        'androidx_core_ktx = { module = '
        +
        '"androidx.core:core-ktx", '
        +
        'version.ref = "core_ktx" }\n'
    )

    return root


def test_core_ktx_pin():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        result = (
            AndroidDependencyCompatibility()
            .repair(
                root
            )
        )

        assert result[
            "changed"
        ]

        assert (
            result[
                "before"
            ][
                "core_ktx"
            ]
            ==
            "1.19.0"
        )

        assert (
            result[
                "after"
            ][
                "core_ktx"
            ]
            ==
            "1.17.0"
        )


def test_core_ktx_pin_idempotent():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        compat = (
            AndroidDependencyCompatibility()
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


def test_agp_other_version_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            agp="8.12.0",
        )

        result = (
            AndroidDependencyCompatibility()
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


def test_compile_sdk_other_version_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            compile_sdk="35",
        )

        result = (
            AndroidDependencyCompatibility()
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


def test_compatible_core_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            core_ktx="1.17.0",
        )

        result = (
            AndroidDependencyCompatibility()
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
