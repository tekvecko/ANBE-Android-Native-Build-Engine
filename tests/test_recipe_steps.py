from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.context import BuildContext
from anbe.recipe import (
    RecipeBuilder,
    RecipeStep,
)


def test_structured_recipe_generation():

    with TemporaryDirectory(
        prefix="anbe-recipe-v3-"
    ) as tmp:

        root = Path(
            tmp
        )

        (
            root
            /
            "package.json"
        ).write_text(
            '{"scripts":{"build":"echo build"}}'
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

        (
            android
            /
            "gradlew"
        ).write_text(
            "#!/bin/sh\n"
        )

        ctx = BuildContext(
            root
        )

        RecipeBuilder().create(
            ctx
        )

        assert (
            ctx.recipe[
                "schema"
            ]
            ==
            "anbe.recipe.dynamic.v3"
        )

        steps = ctx.recipe[
            "steps"
        ]

        assert len(
            steps
        ) == 5

        assert all(
            isinstance(
                step,
                dict
            )
            for step in steps
        )

        assert all(
            step.get(
                "schema"
            )
            ==
            RecipeStep.SCHEMA
            for step in steps
        )

        ids = [
            step[
                "id"
            ]
            for step in steps
        ]

        assert ids == [
            "npm-install",
            "npm-build",
            "capacitor-sync-android",
            "android-prepare",
            "gradle-assembledebug",
        ]

        assert (
            steps[-1][
                "type"
            ]
            ==
            "gradle"
        )

        assert (
            steps[-1][
                "task"
            ]
            ==
            "assembleDebug"
        )


        dependency_map = {
            step["id"]:
            step.get(
                "depends_on",
                []
            )
            for step in steps
        }

        assert dependency_map == {
            "npm-install": [],
            "npm-build": [
                "npm-install"
            ],
            "capacitor-sync-android": [
                "npm-build"
            ],
            "android-prepare": [
                "capacitor-sync-android"
            ],
            "gradle-assembledebug": [
                "android-prepare"
            ],
        }


def test_legacy_recipe_normalization():

    legacy = [
        "npm install",
        "npm run build",
        "npx cap sync android",
        "android prepare",
        "gradle assembleDebug",
    ]

    steps = (
        RecipeStep.normalize_all(
            legacy
        )
    )

    assert [
        step[
            "type"
        ]
        for step in steps
    ] == [
        "command",
        "command",
        "command",
        "android_prepare",
        "gradle",
    ]

    assert (
        steps[-1][
            "task"
        ]
        ==
        "assembleDebug"
    )


def test_invalid_recipe_step_rejected():

    bad = {
        "id":
        "broken",

        "type":
        "gradle",
    }

    try:

        RecipeStep.assert_valid(
            bad
        )

    except ValueError:

        return

    raise AssertionError(
        "Invalid recipe step accepted"
    )


if __name__ == "__main__":

    test_structured_recipe_generation()
    print(
        "Structured recipe regression OK"
    )

    test_legacy_recipe_normalization()
    print(
        "Legacy recipe compatibility OK"
    )

    test_invalid_recipe_step_rejected()
    print(
        "Invalid recipe rejection OK"
    )
