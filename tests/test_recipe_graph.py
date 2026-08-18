from anbe.recipe import (
    RecipeGraph,
    RecipeStep,
)


def test_dependency_topological_sort():

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
        RecipeGraph.topological_sort(
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


def test_stable_topological_order():

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

    ordered = (
        RecipeGraph.topological_sort(
            steps
        )
    )

    assert [
        step["id"]
        for step in ordered
    ] == [
        "first",
        "second",
        "third",
    ]


def test_missing_dependency_rejected():

    steps = [
        RecipeStep.command(
            "compile",
            "echo compile",
            depends_on=[
                "missing"
            ],
        ),
    ]

    errors = (
        RecipeGraph.validate(
            steps
        )
    )

    assert errors

    assert any(
        "missing step"
        in error
        for error in errors
    )


def test_cycle_rejected():

    steps = [
        RecipeStep.command(
            "a",
            "echo a",
            depends_on=[
                "b"
            ],
        ),

        RecipeStep.command(
            "b",
            "echo b",
            depends_on=[
                "a"
            ],
        ),
    ]

    errors = (
        RecipeGraph.validate(
            steps
        )
    )

    assert errors

    assert any(
        "cycle"
        in error
        for error in errors
    )


def test_duplicate_ids_rejected():

    steps = [
        RecipeStep.command(
            "same",
            "echo one",
        ),

        RecipeStep.command(
            "same",
            "echo two",
        ),
    ]

    errors = (
        RecipeGraph.validate(
            steps
        )
    )

    assert errors

    assert any(
        "duplicate step ids"
        in error
        for error in errors
    )


if __name__ == "__main__":

    test_dependency_topological_sort()
    print(
        "Dependency ordering regression OK"
    )

    test_stable_topological_order()
    print(
        "Stable ordering regression OK"
    )

    test_missing_dependency_rejected()
    print(
        "Missing dependency rejection OK"
    )

    test_cycle_rejected()
    print(
        "Cycle rejection OK"
    )

    test_duplicate_ids_rejected()
    print(
        "Duplicate step rejection OK"
    )
