#!/usr/bin/env python3

from tests.test_framework_regression import (
    test_java_resolver,
    test_recipe_android_discovery,
    test_pipeline_stage_contract,
)

from tests.test_toolchain_regression import (
    test_aapt2_runtime,
    test_gradle_command_wiring,
)

from tests.test_artifact_regression import (
    test_artifact_detect_and_export,
)

from tests.test_verifier_regression import (
    test_build_verifier_success,
    test_build_verifier_rejects_missing_artifact,
)

from tests.test_preflight_regression import (
    test_preflight_ready,
    test_preflight_rejects_missing_project,
)



from tests.test_context_schema import (
    test_context_schema_valid,
    test_context_snapshot,
    test_context_schema_rejects_corruption,
)


from tests.test_recipe_steps import (
    test_structured_recipe_generation,
    test_legacy_recipe_normalization,
    test_invalid_recipe_step_rejected,
)


from tests.test_recipe_graph import (
    test_dependency_topological_sort,
    test_stable_topological_order,
    test_missing_dependency_rejected,
    test_cycle_rejected,
    test_duplicate_ids_rejected,
)


from tests.test_execution_planner import (
    test_execution_waves,
    test_execution_plan_stable,
    test_gradle_not_parallel_safe,
    test_planner_preserves_dependency_order,
    test_real_android_recipe_plan,
)

def run():

    checks = [
        (
            "Execution waves",
            test_execution_waves,
        ),
        (
            "Execution plan stability",
            test_execution_plan_stable,
        ),
        (
            "Exclusive Gradle scheduling",
            test_gradle_not_parallel_safe,
        ),
        (
            "Planner dependency ordering",
            test_planner_preserves_dependency_order,
        ),
        (
            "Android recipe execution plan",
            test_real_android_recipe_plan,
        ),
        (
            "Dependency ordering",
            test_dependency_topological_sort,
        ),
        (
            "Stable dependency ordering",
            test_stable_topological_order,
        ),
        (
            "Missing dependency rejection",
            test_missing_dependency_rejected,
        ),
        (
            "Dependency cycle rejection",
            test_cycle_rejected,
        ),
        (
            "Duplicate step rejection",
            test_duplicate_ids_rejected,
        ),
        (
            "Structured recipe",
            test_structured_recipe_generation,
        ),
        (
            "Legacy recipe compatibility",
            test_legacy_recipe_normalization,
        ),
        (
            "Recipe validation",
            test_invalid_recipe_step_rejected,
        ),
        (
            "BuildContext schema",
            test_context_schema_valid,
        ),
        (
            "BuildContext snapshot",
            test_context_snapshot,
        ),
        (
            "BuildContext corruption rejection",
            test_context_schema_rejects_corruption,
        ),
        (
            "JavaResolver",
            test_java_resolver,
        ),
        (
            "Recipe discovery",
            test_recipe_android_discovery,
        ),
        (
            "Pipeline contract",
            test_pipeline_stage_contract,
        ),
        (
            "AAPT2 runtime",
            test_aapt2_runtime,
        ),
        (
            "Gradle wiring",
            test_gradle_command_wiring,
        ),
        (
            "Artifact detect/export",
            test_artifact_detect_and_export,
        ),
        (
            "Build verifier success",
            test_build_verifier_success,
        ),
        (
            "Build verifier rejection",
            test_build_verifier_rejects_missing_artifact,
        ),
        (
            "Preflight ready",
            test_preflight_ready,
        ),
        (
            "Preflight rejection",
            test_preflight_rejects_missing_project,
        ),
    ]

    print()
    print("=" * 48)
    print("ANBE REGRESSION SUITE")
    print("=" * 48)

    for name, fn in checks:

        print()
        print(
            "[TEST]",
            name
        )

        fn()

        print(
            "[PASS]",
            name
        )

    print()
    print("=" * 48)
    print(
        "ALL ANBE REGRESSION TESTS PASSED"
    )
    print("=" * 48)


if __name__ == "__main__":
    run()
