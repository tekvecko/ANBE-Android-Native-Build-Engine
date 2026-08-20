from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.context import BuildContext
from anbe.signing_bridge import SigningBridge


SOURCE = '''apply plugin: 'com.android.application'

android {
    namespace "example.app"

    defaultConfig {
        applicationId "example.app"
    }

    buildTypes {
        release {
            minifyEnabled false
        }
    }
}
'''


def test_signing_bridge_injection():

    with TemporaryDirectory(
        prefix="anbe-signing-"
    ) as tmp:

        root = Path(
            tmp
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

        gradle = (
            app
            /
            "build.gradle"
        )

        gradle.write_text(
            SOURCE
        )

        ctx = BuildContext(
            root
        )

        ctx.build_mode = "release"

        SigningBridge().apply(
            ctx
        )

        text = gradle.read_text()

        assert (
            "ANBE_RELEASE_STORE_FILE"
            in text
        )

        assert (
            "signingConfigs"
            in text
        )

        assert (
            "signingConfig signingConfigs.anbeRelease"
            in text
        )


def test_signing_bridge_idempotent():

    with TemporaryDirectory(
        prefix="anbe-signing-idempotent-"
    ) as tmp:

        root = Path(
            tmp
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

        gradle = (
            app
            /
            "build.gradle"
        )

        gradle.write_text(
            SOURCE
        )

        ctx = BuildContext(
            root
        )

        ctx.build_mode = "release"

        bridge = SigningBridge()

        bridge.apply(
            ctx
        )

        first = (
            gradle.read_text()
        )

        bridge.apply(
            ctx
        )

        second = (
            gradle.read_text()
        )

        assert first == second


if __name__ == "__main__":

    test_signing_bridge_injection()
    print(
        "Signing bridge injection OK"
    )

    test_signing_bridge_idempotent()
    print(
        "Signing bridge idempotency OK"
    )
