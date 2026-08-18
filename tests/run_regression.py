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
    ]

    print()
    print("=" * 48)
    print("ANBE REGRESSION SUITE")
    print("=" * 48)

    for name, fn in checks:

        print()
        print("[TEST]", name)

        fn()

        print("[PASS]", name)

    print()
    print("=" * 48)
    print("ALL ANBE REGRESSION TESTS PASSED")
    print("=" * 48)


if __name__ == "__main__":
    run()
