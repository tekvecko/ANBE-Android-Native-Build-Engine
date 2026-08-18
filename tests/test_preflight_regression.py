from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.preflight import Preflight


class FakeJavaResolver:

    def gradle_version(
        self,
        root
    ):

        return "8.2"


    def required_java(
        self,
        root
    ):

        return 21


    def resolve(
        self,
        root
    ):

        return (
            "/fake/java-21-openjdk"
        )


class FakeAndroidToolchain:

    def resolve(self):

        return {
            "aapt2":
            "/fake/aapt2",

            "aidl":
            "/fake/aidl",

            "zipalign":
            "/fake/zipalign",

            "apksigner":
            "/fake/apksigner",
        }


def fake_which(
    name
):

    return (
        "/fake/bin/"
        +
        name
    )


def test_preflight_ready():

    with TemporaryDirectory(
        prefix="anbe-preflight-"
    ) as tmp:

        root = Path(
            tmp
        )

        (
            root
            /
            "capacitor.config.json"
        ).write_text(
            "{}"
        )

        android = (
            root
            /
            "android"
        )

        android.mkdir()

        gradlew = (
            android
            /
            "gradlew"
        )

        gradlew.write_text(
            "#!/bin/sh\n"
        )

        engine = Preflight(
            java_resolver=(
                FakeJavaResolver()
            ),
            android_toolchain=(
                FakeAndroidToolchain()
            ),
            which=fake_which,
        )

        report = engine.inspect(
            root
        )

        assert (
            report["framework"]
            ==
            "capacitor"
        )

        assert (
            report["android_root"]
            ==
            "android"
        )

        assert (
            report["ready"]
            is True
        )

        assert (
            report["errors"]
            ==
            []
        )


def test_preflight_rejects_missing_project():

    engine = Preflight(
        java_resolver=(
            FakeJavaResolver()
        ),
        android_toolchain=(
            FakeAndroidToolchain()
        ),
        which=fake_which,
    )

    report = engine.inspect(
        "/definitely/not/anbe/project"
    )

    assert (
        report["ready"]
        is False
    )

    assert (
        report["errors"]
    )


if __name__ == "__main__":

    test_preflight_ready()

    print(
        "Preflight ready regression OK"
    )

    test_preflight_rejects_missing_project()

    print(
        "Preflight rejection regression OK"
    )

    print(
        "ANBE preflight regression suite OK"
    )
