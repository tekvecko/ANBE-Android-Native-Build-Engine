from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from anbe.context import BuildContext
from anbe.recipe import RecipeBuilder
from anbe.release_signing import ReleaseSigning


def make_project(
    root
):

    (
        root
        /
        "package.json"
    ).write_text(
        '{"scripts":{"build":"echo build"}}'
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


def test_debug_recipe_unchanged():

    with TemporaryDirectory(
        prefix="anbe-release-debug-"
    ) as tmp:

        root = Path(tmp)

        make_project(
            root
        )

        ctx = BuildContext(
            root
        )

        RecipeBuilder().create(
            ctx
        )

        assert (
            ctx.recipe[
                "build"
            ][
                "gradle_task"
            ]
            ==
            "assembleDebug"
        )

        assert (
            ctx.recipe[
                "artifact"
            ][
                "path"
            ]
            ==
            "android/app/build/outputs/"
            "apk/debug/app-debug.apk"
        )


def test_release_apk_recipe():

    with TemporaryDirectory(
        prefix="anbe-release-apk-"
    ) as tmp:

        root = Path(tmp)

        make_project(
            root
        )

        ctx = BuildContext(
            root
        )

        ctx.build_mode = "release"
        ctx.artifact_format = "apk"

        with patch.dict(
            "os.environ",
            {
                "ANBE_KEYSTORE": "",
                "ANBE_KEYSTORE_PASSWORD": "",
                "ANBE_KEY_ALIAS": "",
                "ANBE_KEY_PASSWORD": "",
            },
        ):

            RecipeBuilder().create(
                ctx
            )

        assert (
            ctx.recipe[
                "build"
            ][
                "gradle_task"
            ]
            ==
            "assembleRelease"
        )

        assert (
            ctx.recipe[
                "artifact"
            ][
                "path"
            ]
            ==
            "android/app/build/outputs/"
            "apk/release/app-release-unsigned.apk"
        )


def test_release_aab_recipe():

    with TemporaryDirectory(
        prefix="anbe-release-aab-"
    ) as tmp:

        root = Path(tmp)

        make_project(
            root
        )

        ctx = BuildContext(
            root
        )

        ctx.build_mode = "release"
        ctx.artifact_format = "aab"

        RecipeBuilder().create(
            ctx
        )

        assert (
            ctx.recipe[
                "build"
            ][
                "gradle_task"
            ]
            ==
            "bundleRelease"
        )

        assert (
            ctx.recipe[
                "artifact"
            ][
                "type"
            ]
            ==
            "aab"
        )

        assert (
            ctx.recipe[
                "artifact"
            ][
                "path"
            ]
            ==
            "android/app/build/outputs/"
            "bundle/release/app-release.aab"
        )


def test_signing_missing_is_safe():

    status = (
        ReleaseSigning()
        .validate()
    )

    assert isinstance(
        status,
        dict
    )

    assert (
        "configured"
        in status
    )


if __name__ == "__main__":

    test_debug_recipe_unchanged()
    print(
        "Debug compatibility OK"
    )

    test_release_apk_recipe()
    print(
        "Release APK recipe OK"
    )

    test_release_aab_recipe()
    print(
        "Release AAB recipe OK"
    )

    test_signing_missing_is_safe()
    print(
        "Release signing safety OK"
    )
