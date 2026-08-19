# ANBE Support

## Before opening an issue

Run:

```bash
anbe --version
anbe doctor <project>
```

If possible also run:

```bash
python -m tests.run_ci
```

## Bug reports

Please include:

- ANBE version
- Android / Termux version
- device architecture
- Python version
- Java version
- Gradle version
- project framework
- command used
- relevant error output

Remove passwords, tokens, keystores and other secrets before posting logs.

## Security issues

Security-sensitive problems should follow `SECURITY.md` instead of a
normal public bug report.

## Project scope

The stable supported environment is currently Android / Termux / ARM64
with Capacitor Android projects.

Reports from other environments are still useful, but may be classified
as experimental support.
