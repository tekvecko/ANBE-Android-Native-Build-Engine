#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.protobuf_compatibility import ProtobufCompatibility


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


class CompatWithProtoc(
    ProtobufCompatibility
):

    def system_protoc(
        self,
    ):

        return (
            "/data/data/com.termux/"
            "files/usr/bin/protoc"
        )


def make_project(
    root,
):

    root = Path(
        root
    )

    module = (
        root
        /
        "core"
        /
        "datastore-proto"
    )

    module.mkdir(
        parents=True
    )

    build = (
        module
        /
        "build.gradle.kts"
    )

    build.write_text(
        "plugins {\n"
        "    id(\"com.google.protobuf\")\n"
        "}\n"
        "\n"
        "protobuf {\n"
        "    protoc {\n"
        "        artifact = "
        "libs.protobuf.protoc.get().toString()\n"
        "    }\n"
        "}\n"
    )

    return root, build


def test_termux_protoc_repair():

    with TemporaryDirectory() as tmp:

        root, build = make_project(
            tmp
        )

        compat = CompatWithProtoc(
            host_environment=TermuxHost()
        )

        result = compat.repair(
            root
        )

        assert result[
            "changed"
        ]

        text = build.read_text()

        assert (
            'path = "/data/data/com.termux/files/usr/bin/protoc"'
            in text
        )

        assert (
            "artifact ="
            not in text
        )


def test_termux_protoc_repair_idempotent():

    with TemporaryDirectory() as tmp:

        root, build = make_project(
            tmp
        )

        compat = CompatWithProtoc(
            host_environment=TermuxHost()
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


def test_non_termux_unchanged():

    with TemporaryDirectory() as tmp:

        root, build = make_project(
            tmp
        )

        original = build.read_text()

        result = (
            CompatWithProtoc(
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

        assert (
            build.read_text()
            ==
            original
        )
