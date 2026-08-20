#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.artifact.engine import ArtifactEngine


class Context:

    def __init__(
        self,
        path,
        build_mode="debug",
    ):

        self.path = str(
            path
        )

        self.build_mode = (
            build_mode
        )


def make_git_project(
    root,
    remote,
):

    root = Path(
        root
    )

    git = (
        root
        /
        ".git"
    )

    git.mkdir()

    (
        git
        /
        "config"
    ).write_text(
        "[remote \"origin\"]\n"
        "    url = "
        +
        remote
        +
        "\n"
    )

    return root


def test_repository_name_https():

    with TemporaryDirectory() as tmp:

        root = make_git_project(
            tmp,
            (
                "https://github.com/"
                "cortinico/"
                "kotlin-android-template.git"
            ),
        )

        ctx = Context(
            root
        )

        name = (
            ArtifactEngine()
            .repository_name(
                ctx
            )
        )

        assert (
            name
            ==
            "kotlin-android-template"
        )


def test_repository_name_ssh():

    with TemporaryDirectory() as tmp:

        root = make_git_project(
            tmp,
            (
                "git@github.com:"
                "example/"
                "my-app.git"
            ),
        )

        ctx = Context(
            root
        )

        assert (
            ArtifactEngine()
            .repository_name(
                ctx
            )
            ==
            "my-app"
        )


def test_debug_export_name():

    with TemporaryDirectory() as tmp:

        root = make_git_project(
            tmp,
            (
                "https://github.com/"
                "example/"
                "demo-project.git"
            ),
        )

        ctx = Context(
            root,
            build_mode="debug",
        )

        name = (
            ArtifactEngine()
            .export_name(
                ctx,
                Path(
                    "app-debug.apk"
                ),
            )
        )

        assert (
            name
            ==
            "demo-project.apk"
        )


def test_release_export_name():

    with TemporaryDirectory() as tmp:

        root = make_git_project(
            tmp,
            (
                "https://github.com/"
                "example/"
                "demo-project.git"
            ),
        )

        ctx = Context(
            root,
            build_mode="release",
        )

        name = (
            ArtifactEngine()
            .export_name(
                ctx,
                Path(
                    "app-release.apk"
                ),
            )
        )

        assert (
            name
            ==
            "demo-project-release.apk"
        )


def test_folder_fallback():

    with TemporaryDirectory(
        prefix="anbe-project-"
    ) as tmp:

        root = Path(
            tmp
        )

        ctx = Context(
            root
        )

        name = (
            ArtifactEngine()
            .repository_name(
                ctx
            )
        )

        assert name
        assert "/" not in name
