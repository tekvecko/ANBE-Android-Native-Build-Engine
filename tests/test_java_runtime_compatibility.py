#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.java_resolver import JavaResolver


class FakeResolver(JavaResolver):

    def __init__(
        self,
        installed,
    ):

        self.installed = set(
            installed
        )

        self.termux_jvm = Path(
            "/fake/jvm"
        )


    def find_java(
        self,
        version,
    ):

        if version in self.installed:

            return Path(
                "/fake/jvm/"
                +
                "java-"
                +
                str(version)
                +
                "-openjdk"
            )

        return None


def make_gradle(
    root,
    version,
    java_target=None,
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
        "https\\://services.gradle.org/"
        "distributions/"
        "gradle-"
        +
        version
        +
        "-bin.zip\n"
    )

    if java_target is not None:

        (
            root
            /
            "build.gradle"
        ).write_text(
            "android {\n"
            "  compileOptions {\n"
            "    sourceCompatibility "
            "JavaVersion.VERSION_"
            +
            str(java_target)
            +
            "\n"
            "  }\n"
            "}\n"
        )

    return root


def test_gradle75_uses_java17():

    with TemporaryDirectory() as tmp:

        root = make_gradle(
            tmp,
            "7.5",
            java_target=11,
        )

        resolver = FakeResolver({
            17,
            21,
        })

        assert (
            resolver.resolve(
                root
            )
            ==
            "/fake/jvm/java-17-openjdk"
        )


def test_gradle82_java21_project_stays_java21():

    with TemporaryDirectory() as tmp:

        root = make_gradle(
            tmp,
            "8.2",
            java_target=21,
        )

        resolver = FakeResolver({
            17,
            21,
        })

        assert (
            resolver.resolve(
                root
            )
            ==
            "/fake/jvm/java-21-openjdk"
        )


def test_gradle75_never_selects_java21():

    with TemporaryDirectory() as tmp:

        root = make_gradle(
            tmp,
            "7.5",
        )

        resolver = FakeResolver({
            21,
        })

        assert (
            resolver.resolve(
                root
            )
            is None
        )


def test_gradle85_can_use_java21():

    with TemporaryDirectory() as tmp:

        root = make_gradle(
            tmp,
            "8.5",
            java_target=21,
        )

        resolver = FakeResolver({
            21,
        })

        assert (
            resolver.resolve(
                root
            )
            ==
            "/fake/jvm/java-21-openjdk"
        )
