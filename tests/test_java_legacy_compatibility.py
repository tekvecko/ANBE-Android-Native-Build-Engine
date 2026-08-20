#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.java_resolver import JavaResolver


class FakeResolver(JavaResolver):

    def __init__(
        self,
        available,
    ):

        super().__init__()

        self.available = set(
            available
        )


    def find_java(
        self,
        version,
    ):

        if version in self.available:

            return Path(
                "/fake"
            ) / (
                "java-"
                +
                str(version)
                +
                "-openjdk"
            )

        return None


def make_project(
    root,
    gradle,
    java_line=None,
):

    root = Path(
        root
    )

    wrapper = (
        root
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
        "distributionUrl="
        "https\\://services.gradle.org/distributions/"
        "gradle-"
        +
        gradle
        +
        "-bin.zip\\n"
    )

    if java_line:

        (
            root
            /
            "build.gradle"
        ).write_text(
            java_line
            +
            "\n"
        )

    return root


def test_legacy_java8_parsing():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            "7.0",
            (
                "sourceCompatibility "
                "JavaVersion.VERSION_1_8"
            ),
        )

        resolver = JavaResolver()

        assert (
            resolver.project_java_version(
                root
            )
            ==
            8
        )


def test_gradle70_runtime_max_java16():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            "7.0",
        )

        assert (
            JavaResolver()
            .gradle_runtime_max_java(
                root
            )
            ==
            16
        )


def test_gradle70_rejects_only_java17_and_21():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            "7.0",
            (
                "sourceCompatibility "
                "JavaVersion.VERSION_1_8"
            ),
        )

        resolver = FakeResolver({
            17,
            21,
        })

        assert (
            resolver.runtime_java(
                root
            )
            is None
        )


def test_gradle70_can_select_java11():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            "7.0",
            (
                "sourceCompatibility "
                "JavaVersion.VERSION_1_8"
            ),
        )

        resolver = FakeResolver({
            11,
            17,
            21,
        })

        assert (
            str(
                resolver.runtime_java(
                    root
                )
            )
            .endswith(
                "java-11-openjdk"
            )
        )


def test_gradle73_can_select_java17():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            "7.3",
            (
                "sourceCompatibility "
                "JavaVersion.VERSION_17"
            ),
        )

        resolver = FakeResolver({
            17,
            21,
        })

        assert (
            str(
                resolver.runtime_java(
                    root
                )
            )
            .endswith(
                "java-17-openjdk"
            )
        )
