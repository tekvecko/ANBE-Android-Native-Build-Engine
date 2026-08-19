# ANBE

**Autonomous Android build and release engine.**

ANBE turns a supported project into a verified Android artifact without
requiring the user to manually orchestrate Node, Capacitor, Gradle, Java,
AAPT2, artifact discovery, signing and release verification.

The first stable open-source release focuses on **Capacitor Android
projects running locally in Termux on Android/ARM64**.

## What ANBE does

```text
Project
  ↓
Detect
  ↓
Analyze
  ↓
Plan
  ↓
Repair
  ↓
Build
  ↓
Verify
  ↓
Sign / inspect
  ↓
Export APK or AAB
  ↓
Launch readiness report
```

ANBE is not a replacement for Gradle.

It is an orchestration, diagnostics and release layer around the Android
build toolchain.

## Features

- Capacitor project detection
- Java / Gradle compatibility resolution
- Android toolchain preflight diagnostics
- Termux ARM64 AAPT2 support
- structured build recipes
- recipe dependency graph
- dependency-aware execution planning
- build repair pipeline
- debug APK builds
- release APK builds
- Android App Bundle (`.aab`) builds
- secure release signing through environment variables
- APK signature verification
- signer certificate SHA-256 reporting
- artifact verification and export
- JSON/TXT launch readiness reports
- portable CI and regression suites

## Supported environment

The currently verified stable path is:

- Android / Termux
- ARM64 / aarch64
- Python 3.12+
- Node.js / npm / npx where required
- Gradle-based Android project
- Capacitor Android application

Other project types should currently be treated as experimental unless
explicitly documented.

## Installation

```bash
git clone https://github.com/tekvecko/ANBE-Android-Native-Build-Engine.git
cd ANBE-Android-Native-Build-Engine
./install.sh
```

Verify:

```bash
anbe --version
```

## Quick start

Check project readiness:

```bash
anbe doctor ~/my-project
```

Build debug APK:

```bash
anbe build ~/my-project
```

Build release APK:

```bash
anbe release ~/my-project
```

Build release AAB:

```bash
anbe release ~/my-project --aab
```

Run the complete launch flow:

```bash
anbe launch ~/my-project
```

Or produce an AAB:

```bash
anbe launch ~/my-project --aab
```

## Release signing

ANBE does not store signing secrets in the repository.

Configure release signing through environment variables:

```bash
export ANBE_KEYSTORE="$HOME/.anbe/keys/release.jks"
export ANBE_KEYSTORE_PASSWORD="..."
export ANBE_KEY_ALIAS="..."
export ANBE_KEY_PASSWORD="..."
```

Never commit keystores or passwords to Git.

## ANBE Launch

`anbe launch` produces a release artifact together with a readiness report.

The report can contain:

- application ID
- version code
- version name
- artifact path
- artifact size
- artifact SHA-256
- signing state
- signer certificate fingerprint for APK
- release readiness score

Example:

```text
ANBE LAUNCH
================================================
Application: com.example.app
Artifact: .../anbe-release.apk
Readiness: 100/100 READY
JSON report: reports/launch-report-....json
TXT report: reports/launch-report-....txt
```

## Development

```bash
python -m compileall -q anbe tests
python -m tests.run_ci
python -m tests.run_regression
```

## Security

See `SECURITY.md`.

## Contributing

See `CONTRIBUTING.md`.

## License

Apache License 2.0.

See `LICENSE`.
