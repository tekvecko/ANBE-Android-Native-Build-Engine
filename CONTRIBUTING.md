# Contributing to ANBE

Thank you for helping improve ANBE.

## Development checks

Before submitting a change:

```bash
python -m compileall -q anbe tests
python -m tests.run_ci
python -m tests.run_regression
```

## Design principles

Changes should preserve:

1. deterministic builds,
2. explicit contracts,
3. backward compatibility where practical,
4. signing-secret isolation,
5. useful diagnostics,
6. regression coverage.

## Do not commit

- keystores
- passwords
- API tokens
- APK/AAB files
- runtime installations
- project-specific secrets
