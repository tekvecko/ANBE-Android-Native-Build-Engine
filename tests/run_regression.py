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


def run():

    checks = [
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
