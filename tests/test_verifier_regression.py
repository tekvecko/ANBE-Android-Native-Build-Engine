from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.context import BuildContext
from anbe.artifact import ArtifactEngine
from anbe.build_verifier import BuildVerifier


def test_build_verifier_success():

    with TemporaryDirectory(
        prefix="anbe-verify-test-"
    ) as tmp:

        root = Path(
            tmp
        )

        apk = (
            root
            / "android"
            / "app"
            / "build"
            / "outputs"
            / "apk"
            / "debug"
            / "app-debug.apk"
        )

        apk.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        apk.write_bytes(
            b"ANBE-APK"
        )

        ctx = BuildContext(
            root
        )

        ctx.recipe = {
            "artifact": {
                "type":
                "apk",

                "path":
                "android/app/build/outputs/apk/debug/app-debug.apk"
            }
        }

        ctx.execution = [
            {
                "command":
                "./gradlew assembleDebug",

                "success":
                True,

                "returncode":
                0,
            }
        ]

        ArtifactEngine().detect(
            ctx
        )

        BuildVerifier().verify(
            ctx
        )

        assert (
            ctx.meta[
                "verification"
            ][
                "success"
            ]
            is True
        )


def test_build_verifier_rejects_missing_artifact():

    with TemporaryDirectory(
        prefix="anbe-verify-fail-"
    ) as tmp:

        root = Path(
            tmp
        )

        ctx = BuildContext(
            root
        )

        ctx.recipe = {
            "artifact": {
                "type":
                "apk",

                "path":
                "android/app/build/outputs/apk/debug/app-debug.apk"
            }
        }

        try:

            BuildVerifier().verify(
                ctx
            )

        except RuntimeError:

            return

        raise AssertionError(
            "BuildVerifier accepted missing artifact"
        )


if __name__ == "__main__":

    test_build_verifier_success()

    print(
        "Build verifier success regression OK"
    )

    test_build_verifier_rejects_missing_artifact()

    print(
        "Build verifier failure regression OK"
    )

    print(
        "ANBE build verifier regression suite OK"
    )
