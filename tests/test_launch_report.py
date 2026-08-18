from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.context import BuildContext
from anbe.launch_report import LaunchReport


GRADLE = '''apply plugin: 'com.android.application'

android {
    namespace "com.example.launch"

    defaultConfig {
        applicationId "com.example.launch"
        versionCode 7
        versionName "2.0.0"
    }
}
'''


def fixture():

    tmp = TemporaryDirectory(
        prefix="anbe-launch-"
    )

    root = Path(
        tmp.name
    )

    app = (
        root
        /
        "android"
        /
        "app"
    )

    app.mkdir(
        parents=True
    )

    (
        app
        /
        "build.gradle"
    ).write_text(
        GRADLE
    )

    artifact = (
        root
        /
        "release.apk"
    )

    artifact.write_bytes(
        b"ANBE-LAUNCH-APK"
    )

    ctx = BuildContext(
        root
    )

    ctx.build_mode = "release"
    ctx.artifact_format = "apk"

    ctx.recipe = {
        "android_root":
        "android"
    }

    ctx.exports = [
        artifact
    ]

    ctx.meta[
        "verification"
    ] = {
        "success":
        True
    }

    ctx.meta[
        "release_signature"
    ] = {
        "checked":
        True,

        "verified":
        True,

        "certificate_sha256":
        "abc123",
    }

    return (
        tmp,
        ctx,
    )


def test_launch_identity():

    tmp, ctx = fixture()

    try:

        identity = (
            LaunchReport()
            .app_identity(
                ctx
            )
        )

        assert (
            identity[
                "application_id"
            ]
            ==
            "com.example.launch"
        )

        assert (
            identity[
                "version_code"
            ]
            ==
            7
        )

        assert (
            identity[
                "version_name"
            ]
            ==
            "2.0.0"
        )

    finally:

        tmp.cleanup()


def test_launch_artifact_metadata():

    tmp, ctx = fixture()

    try:

        info = (
            LaunchReport()
            .artifact_info(
                ctx
            )
        )

        assert info[
            "format"
        ] == "apk"

        assert (
            info[
                "size_bytes"
            ]
            >
            0
        )

        assert len(
            info[
                "sha256"
            ]
        ) == 64

    finally:

        tmp.cleanup()


def test_launch_readiness_ready():

    tmp, ctx = fixture()

    try:

        engine = (
            LaunchReport()
        )

        identity = (
            engine.app_identity(
                ctx
            )
        )

        artifact = (
            engine.artifact_info(
                ctx
            )
        )

        signing = (
            engine.signing_info(
                ctx
            )
        )

        readiness = (
            engine.readiness(
                ctx,
                identity,
                artifact,
                signing,
            )
        )

        assert (
            readiness[
                "score"
            ]
            ==
            100
        )

        assert (
            readiness[
                "status"
            ]
            ==
            "READY"
        )

    finally:

        tmp.cleanup()


if __name__ == "__main__":

    test_launch_identity()
    print(
        "Launch identity regression OK"
    )

    test_launch_artifact_metadata()
    print(
        "Launch artifact metadata OK"
    )

    test_launch_readiness_ready()
    print(
        "Launch readiness regression OK"
    )
