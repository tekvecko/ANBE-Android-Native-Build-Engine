#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.context import BuildContext
from anbe.recipe.engine import RecipeEngine


def make_android_project(
    root,
    with_demo=False,
):

    root = Path(
        root
    )

    (
        root
        /
        "gradlew"
    ).write_text(
        "#!/bin/sh\n"
    )

    (
        root
        /
        "settings.gradle.kts"
    ).write_text(
        'rootProject.name = "test"\n'
        'include(":app")\n'
    )

    app = (
        root
        /
        "app"
    )

    app.mkdir()

    (
        app
        /
        "build.gradle.kts"
    ).write_text(
        'plugins { id("com.android.application") }\n'
    )

    if with_demo:

        build_logic = (
            root
            /
            "build-logic"
            /
            "src"
            /
            "main"
            /
            "kotlin"
        )

        build_logic.mkdir(
            parents=True
        )

        (
            build_logic
            /
            "Flavor.kt"
        ).write_text(
            'enum class NiaFlavor {\n'
            '    demo(FlavorDimension.contentType),\n'
            '    prod(FlavorDimension.contentType),\n'
            '}\n'
        )

    return root


def test_plain_android_debug_unchanged():

    with TemporaryDirectory() as tmp:

        root = make_android_project(
            tmp,
            with_demo=False,
        )

        ctx = BuildContext(
            root
        )

        ctx.build_mode = "debug"
        ctx.artifact_format = "apk"

        RecipeEngine().generate(
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
            "app/build/outputs/apk/debug/app-debug.apk"
        )


def test_demo_flavor_debug():

    with TemporaryDirectory() as tmp:

        root = make_android_project(
            tmp,
            with_demo=True,
        )

        ctx = BuildContext(
            root
        )

        ctx.build_mode = "debug"
        ctx.artifact_format = "apk"

        RecipeEngine().generate(
            ctx
        )

        assert (
            ctx.recipe[
                "build"
            ][
                "gradle_task"
            ]
            ==
            "assembleDemoDebug"
        )

        assert (
            ctx.recipe[
                "artifact"
            ][
                "path"
            ]
            ==
            (
                "app/build/outputs/apk/demo/"
                "debug/app-demo-debug.apk"
            )
        )


def test_demo_flavor_release_apk():

    with TemporaryDirectory() as tmp:

        root = make_android_project(
            tmp,
            with_demo=True,
        )

        ctx = BuildContext(
            root
        )

        ctx.build_mode = "release"
        ctx.artifact_format = "apk"

        RecipeEngine().generate(
            ctx
        )

        assert (
            ctx.recipe[
                "build"
            ][
                "gradle_task"
            ]
            ==
            "assembleDemoRelease"
        )
