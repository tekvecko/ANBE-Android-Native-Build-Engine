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


from tests.test_release_builder import (
    test_debug_recipe_unchanged,
    test_release_apk_recipe,
    test_release_aab_recipe,
    test_signing_missing_is_safe,
)


from tests.test_signing_bridge import (
    test_signing_bridge_injection,
    test_signing_bridge_idempotent,
)


from tests.test_release_signature_verifier import (
    test_signature_verifier_success,
    test_signature_verifier_failure,
    test_signature_verifier_debug_skip,
    test_signature_verifier_aab_skip,
)


from tests.test_release_secret_safety import (
    test_gradle_command_does_not_contain_secrets,
)


from tests.test_launch_report import (
    test_launch_identity,
    test_launch_artifact_metadata,
    test_launch_readiness_ready,
)

def run():

    checks = [
        (
            "Launch app identity",
            test_launch_identity,
        ),
        (
            "Launch artifact metadata",
            test_launch_artifact_metadata,
        ),
        (
            "Launch readiness",
            test_launch_readiness_ready,
        ),
        (
            "Release secret leakage safety",
            test_gradle_command_does_not_contain_secrets,
        ),
        (
            "Release signature verification",
            test_signature_verifier_success,
        ),
        (
            "Invalid signature rejection",
            test_signature_verifier_failure,
        ),
        (
            "Debug signature skip",
            test_signature_verifier_debug_skip,
        ),
        (
            "AAB signature skip",
            test_signature_verifier_aab_skip,
        ),
        (
            "Signing bridge injection",
            test_signing_bridge_injection,
        ),
        (
            "Signing bridge idempotency",
            test_signing_bridge_idempotent,
        ),
        (
            "Debug release compatibility",
            test_debug_recipe_unchanged,
        ),
        (
            "Release APK recipe",
            test_release_apk_recipe,
        ),
        (
            "Release AAB recipe",
            test_release_aab_recipe,
        ),
        (
            "Release signing safety",
            test_signing_missing_is_safe,
        ),
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
