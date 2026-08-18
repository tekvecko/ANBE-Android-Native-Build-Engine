#!/usr/bin/env python3

from tests.test_context_schema import (
    test_context_schema_valid,
    test_context_snapshot,
    test_context_schema_rejects_corruption,
)

from tests.test_framework_regression import (
    test_pipeline_stage_contract,
)


def run():

    checks = [
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
            "Pipeline architecture contract",
            test_pipeline_stage_contract,
        ),
    ]

    print()
    print("=" * 48)
    print("ANBE PORTABLE CI SUITE")
    print("=" * 48)

    for name, fn in checks:

        print()
        print("[TEST]", name)

        fn()

        print("[PASS]", name)

    print()
    print("=" * 48)
    print("ALL ANBE PORTABLE CI TESTS PASSED")
    print("=" * 48)


if __name__ == "__main__":
    run()
