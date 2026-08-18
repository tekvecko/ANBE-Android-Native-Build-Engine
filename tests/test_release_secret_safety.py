import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from anbe.context import BuildContext
from anbe.executor import Executor
from anbe.release_signing import ReleaseSigning


def test_gradle_command_does_not_contain_secrets():

    with TemporaryDirectory(
        prefix="anbe-secret-safe-"
    ) as tmp:

        root = Path(
            tmp
        )

        android = (
            root
            /
            "android"
        )

        android.mkdir()

        (
            android
            /
            "gradlew"
        ).write_text(
            "#!/bin/sh\n"
        )

        keystore = (
            root
            /
            "release.jks"
        )

        keystore.write_bytes(
            b"TEST"
        )

        ctx = BuildContext(
            root
        )

        ctx.recipe[
            "android_root"
        ] = "android"

        aapt2 = (
            root
            /
            "aapt2"
        )

        aapt2.write_bytes(
            b"TEST"
        )

        ctx.runtime[
            "aapt2"
        ] = str(
            aapt2
        )

        ctx.aapt2 = str(
            aapt2
        )

        env = {
            "ANBE_KEYSTORE":
            str(
                keystore
            ),

            "ANBE_KEYSTORE_PASSWORD":
            "super-secret-store",

            "ANBE_KEY_ALIAS":
            "release",

            "ANBE_KEY_PASSWORD":
            "super-secret-key",
        }

        with (
            patch.dict(
                os.environ,
                env,
                clear=False,
            ),
            patch(
                "anbe.executor.JavaResolver.resolve",
                return_value="/fake/java",
            )
        ):

            command = (
                Executor()
                .gradle_command(
                    ctx,
                    task="assembleRelease",
                )
            )

            assert (
                "super-secret-store"
                not in command
            )

            assert (
                "super-secret-key"
                not in command
            )

            assert (
                "ANBE_RELEASE_STORE_PASSWORD"
                not in command
            )

            assert (
                "ANBE_RELEASE_KEY_PASSWORD"
                not in command
            )

            projected = (
                ReleaseSigning()
                .gradle_environment()
            )

            assert (
                projected[
                    "ORG_GRADLE_PROJECT_ANBE_RELEASE_STORE_PASSWORD"
                ]
                ==
                "super-secret-store"
            )

            assert (
                projected[
                    "ORG_GRADLE_PROJECT_ANBE_RELEASE_KEY_PASSWORD"
                ]
                ==
                "super-secret-key"
            )


if __name__ == "__main__":

    test_gradle_command_does_not_contain_secrets()

    print(
        "Release secret leakage regression OK"
    )
