from anbe.execution_planner import (
    ExecutionPlanner,
)

from anbe.recipe import (
    RecipeStep,
)


def test_execution_waves():

    steps = [
        RecipeStep.command(
            "prepare-a",
            "echo a",
        ),

        RecipeStep.command(
            "prepare-b",
            "echo b",
        ),

        RecipeStep.command(
            "compile",
            "echo compile",
            depends_on=[
                "prepare-a",
                "prepare-b",
            ],
        ),

        RecipeStep.command(
            "package",
            "echo package",
            depends_on=[
                "compile"
            ],
        ),
    ]

    planner = ExecutionPlanner()

    plan = planner.plan(
        steps
    )

    assert plan[
        "schema"
    ] == (
        "anbe.execution.plan.v1"
    )

    assert plan[
        "step_count"
    ] == 4

    assert plan[
        "wave_count"
    ] == 3

    assert [
        wave["steps"]
        for wave in plan["waves"]
    ] == [
        [
            "prepare-a",
            "prepare-b",
        ],
        [
            "compile",
        ],
        [
            "package",
        ],
    ]

    assert (
        plan["waves"][0][
            "parallelizable"
        ]
        is True
    )


def test_execution_plan_stable():

    steps = [
        RecipeStep.command(
            "first",
            "echo first",
        ),

        RecipeStep.command(
            "second",
            "echo second",
        ),

        RecipeStep.command(
            "third",
            "echo third",
            depends_on=[
                "first"
            ],
        ),
    ]

    plan = (
        ExecutionPlanner()
        .plan(
            steps
        )
    )

    assert plan[
        "order"
    ] == [
        "first",
        "second",
        "third",
    ]

    assert plan[
        "waves"
    ][0][
        "steps"
    ] == [
        "first",
        "second",
    ]


def test_gradle_not_parallel_safe():

    steps = [
        RecipeStep.command(
            "assets",
            "echo assets",
        ),

        RecipeStep.gradle(
            "assembleDebug"
        ),
    ]

    plan = (
        ExecutionPlanner()
        .plan(
            steps
        )
    )

    assert len(
        plan[
            "waves"
        ][0][
            "steps"
        ]
    ) == 2

    assert (
        plan[
            "waves"
        ][0][
            "parallelizable"
        ]
        is False
    )

    assert (
        "assets"
        in
        plan[
            "waves"
        ][0][
            "parallel_candidates"
        ]
    )

    assert (
        "gradle-assembledebug"
        not in
        plan[
            "waves"
        ][0][
            "parallel_candidates"
        ]
    )


def test_planner_preserves_dependency_order():

    steps = [
        RecipeStep.command(
            "package",
            "echo package",
            depends_on=[
                "compile"
            ],
        ),

        RecipeStep.command(
            "prepare",
            "echo prepare",
        ),

        RecipeStep.command(
            "compile",
            "echo compile",
            depends_on=[
                "prepare"
            ],
        ),
    ]

    ordered = (
        ExecutionPlanner()
        .ordered_steps(
            steps
        )
    )

    assert [
        step["id"]
        for step in ordered
    ] == [
        "prepare",
        "compile",
        "package",
    ]


if __name__ == "__main__":

    test_execution_waves()
    print(
        "Execution wave regression OK"
    )

    test_execution_plan_stable()
    print(
        "Execution plan stability OK"
    )

    test_gradle_not_parallel_safe()
    print(
        "Exclusive Gradle scheduling OK"
    )

    test_planner_preserves_dependency_order()
    print(
        "Planner dependency ordering OK"
    )


def test_real_android_recipe_plan():

    from pathlib import Path
    from tempfile import TemporaryDirectory

    from anbe.context import BuildContext
    from anbe.recipe import RecipeBuilder

    with TemporaryDirectory(
        prefix="anbe-planner-real-"
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

        plan = (
            ExecutionPlanner()
            .plan(
                ctx.recipe[
                    "steps"
                ]
            )
        )

        assert plan[
            "order"
        ] == [
            "npm-install",
            "npm-build",
            "capacitor-sync-android",
            "android-prepare",
            "gradle-assembledebug",
        ]

        assert plan[
            "wave_count"
        ] == 5
