#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from anbe.context import BuildContext
from anbe.executor import Executor


class MissingJavaResolver:

    def resolve(
        self,
        root,
    ):

        return None


    def gradle_version(
        self,
        root,
    ):

        return "7.0"


    def required_java(
        self,
        root,
    ):

        return 8


    def gradle_runtime_max_java(
        self,
        root,
    ):

        return 16


def test_gradle_command_rejects_missing_compatible_java():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        android = (
            root
            /
            "android"
        )

        android.mkdir()

        aapt2 = (
            root
            /
            "aapt2"
        )

        aapt2.write_text(
            ""
        )

        ctx = BuildContext(
            root
        )

        ctx.recipe = {
            "android_root":
            "android"
        }

        ctx.aapt2 = str(
            aapt2
        )

        ctx.runtime[
            "aapt2"
        ] = str(
            aapt2
        )

        with patch(
            "anbe.executor.JavaResolver",
            return_value=MissingJavaResolver(),
        ):

            with pytest.raises(
                RuntimeError,
                match=(
                    "Compatible Java runtime unavailable"
                ),
            ):

                Executor().gradle_command(
                    ctx
                )
