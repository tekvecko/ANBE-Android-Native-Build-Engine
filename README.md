<div align="center">

# ANBE

### Autonomous Android Native Build Engine

**From source project to verified Android release — locally, automatically, reproducibly.**

[![ANBE CI](https://github.com/tekvecko/ANBE-Android-Native-Build-Engine/actions/workflows/ci.yml/badge.svg)](https://github.com/tekvecko/ANBE-Android-Native-Build-Engine/actions/workflows/ci.yml)
[![Latest Release](https://img.shields.io/github/v/release/tekvecko/ANBE-Android-Native-Build-Engine?display_name=tag&sort=semver)](https://github.com/tekvecko/ANBE-Android-Native-Build-Engine/releases)
[![License](https://img.shields.io/github/license/tekvecko/ANBE-Android-Native-Build-Engine)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](pyproject.toml)
[![Platform](https://img.shields.io/badge/platform-Android%20%7C%20Termux%20%7C%20ARM64-green)](#supported-platform)

**[Quick Start](#quick-start) · [Real-world validation](#real-world-validation) · [Launch](#anbe-launch) · [Architecture](docs/ARCHITECTURE.md) · [Roadmap](docs/ROADMAP.md) · [Contributing](CONTRIBUTING.md)**

</div>

---

## Why ANBE?

Building an Android application is often not a single command.

A real project may require project detection, Java / Gradle compatibility resolution, AAPT2 discovery, dependency or host compatibility repair, variant selection, Gradle execution, artifact discovery, signing, verification and export.

ANBE turns that chain into one deterministic pipeline.

> **ANBE is not another Gradle wrapper.** It is an orchestration, diagnostics, repair and release layer around the Android build toolchain.

---

## The shortest version

```bash
anbe doctor ~/my-project
anbe build ~/my-project
```

For the product-oriented release flow:

```bash
anbe launch ~/my-project
```

ANBE analyzes the project, prepares the toolchain, applies narrowly scoped compatibility repairs where required, executes the appropriate Android build, verifies the artifact and exports the result.

---

## Features

### Build intelligence

- automatic project detection
- Capacitor-aware Android discovery
- structured build recipes
- Android product-flavor detection and variant-aware task generation
- dependency graph validation
- dependency-aware execution planning
- deterministic pipeline stages
- formal BuildContext contract
- progress reporting for long-running builds

### Android toolchain

- Java / Gradle runtime compatibility resolution
- Gradle-version-aware JDK selection
- Android preflight diagnostics
- ARM64 AAPT2 discovery and Termux override
- Termux-aware Android execution
- Gradle wrapper preparation and compatibility repair
- Android repair pipeline
- incremental Gradle builds without an implicit `clean` before every invocation

### Self-healing compatibility

ANBE can detect and repair selected build incompatibilities before execution.

Current compatibility work includes:

- package-manager-aware dependency handling
- Termux native dependency compatibility
- Next.js compatibility on Termux, including static-build handling
- case-sensitive JavaScript / TypeScript import repair
- Gradle wrapper compatibility repair
- Gradle runtime JDK compatibility selection
- Capacitor / Android compatibility preparation
- incompatible AndroidX core dependency repair
- native Termux `protoc` fallback for incompatible Maven protobuf compiler binaries
- safe Android launcher icon fallback

Repairs are designed to be deterministic, narrowly scoped and idempotent. Existing compatible projects are left unchanged.

### Release engineering

- debug APK builds
- flavored debug APK builds
- release APK builds
- Android App Bundle (`.aab`) builds
- environment-based signing secrets
- APK signature verification
- signer certificate SHA-256 fingerprint
- artifact SHA-256 calculation
- variant-aware artifact discovery
- repository-aware artifact naming
- release artifact export
- build reports and manifests

### Product layer

- `anbe doctor`
- `anbe build`
- `anbe release`
- `anbe launch`
- JSON release reports
- human-readable TXT reports
- release readiness scoring

### Quality

- portable CI suite
- full regression suite
- regression coverage for product flavors and protobuf compatibility
- isolated Python package installation
- wheel / sdist distribution
- Apache-2.0 licensed

---

## Supported platform

| Component | Status |
|---|---|
| Android / Termux | ✅ Stable |
| ARM64 / aarch64 | ✅ Stable |
| Native Android Gradle projects | ✅ Validated |
| Android product flavors | ✅ Validated |
| Capacitor Android projects | ✅ Stable |
| Python 3.12+ | ✅ Supported |
| Debug APK | ✅ Supported |
| Signed release APK | ✅ Supported |
| Release AAB | ✅ Supported |
| Launch readiness report | ✅ Supported |
| Linux desktop host | 🧪 Experimental |
| macOS | 🧪 Experimental |
| Windows | 🧪 Experimental |
| iOS | ❌ Not supported |

The current stable path is optimized for **Android + Termux + ARM64**.

---

## Real-world validation

### Google Now in Android

ANBE has been validated against **Now in Android**, Google's large real-world Android reference application. This is substantially more demanding than a minimal sample: it is a multi-module Kotlin/Compose project using product flavors and a broad modern Android toolchain.

On an ARM64 Android device running Termux, ANBE successfully completed the project's `DemoDebug` build and produced a working application.

Observed validation result:

```text
Task: :app:assembleDemoDebug
BUILD SUCCESSFUL
912 actionable tasks
APK: app/build/outputs/apk/demo/debug/app-demo-debug.apk
Export: /storage/emulated/0/Download/nowinandroid.apk
Approximate APK size: 36 MB
```

The validation exercised and confirmed several recent ANBE capabilities:

1. product-flavor discovery and selection of `assembleDemoDebug` instead of a generic `assembleDebug` task;
2. variant-aware discovery of the APK under `app/build/outputs/apk/demo/debug/`;
3. Termux protobuf compatibility using the native `protoc` executable when a Maven host binary is unsuitable;
4. Android dependency compatibility repair;
5. preservation of Gradle incremental state by no longer forcing an implicit `clean` before each build;
6. artifact verification, repository-aware naming, export, reporting and manifest generation.

The resulting APK was installed and the Now in Android application ran successfully on the Android device.

This test is an important milestone for ANBE: the engine is not limited to toy or template applications; its Android/Termux path has now been exercised against a substantial production-style open-source Android codebase.

---

## Installation

```bash
git clone https://github.com/tekvecko/ANBE-Android-Native-Build-Engine.git
cd ANBE-Android-Native-Build-Engine
./install.sh
anbe --version
```

---

## Quick start

Diagnose a project:

```bash
anbe doctor ~/my-project
```

Build a debug APK:

```bash
anbe build ~/my-project
```

Build a release APK:

```bash
anbe release ~/my-project
```

Build an Android App Bundle:

```bash
anbe release ~/my-project --aab
```

For flavored Android projects, ANBE can derive the appropriate Gradle task and artifact path from the project configuration rather than assuming only `assembleDebug`.

---

## ANBE Launch

`anbe launch` is the product-oriented release flow.

```bash
anbe launch ~/my-project
```

For an Android App Bundle:

```bash
anbe launch ~/my-project --aab
```

Launch performs the release build and produces release metadata such as application ID, version information, artifact path and size, SHA-256, signing state, signer fingerprint for verified APKs and a release readiness score.

---

## Secure release signing

ANBE does **not** store release passwords in the repository.

```bash
export ANBE_KEYSTORE="$HOME/.anbe/keys/release.jks"
export ANBE_KEYSTORE_PASSWORD="..."
export ANBE_KEY_ALIAS="..."
export ANBE_KEY_PASSWORD="..."
```

Keep the keystore outside project repositories and maintain a secure backup. **Never commit signing credentials or production keystores.**

---

## Local-first by design

ANBE's current stable workflow runs locally. Source code does not need to be uploaded to a third-party build service just to produce an Android artifact.

This makes ANBE useful for independent developers, Android-only environments, Termux workflows, native Android and Capacitor projects, reproducible release automation, build diagnostics and automated compatibility repair.

---

## Architecture

The high-level pipeline currently consists of:

```text
Cache
Detector
Analyzer
Plugin
Profile
ProfileOptimizer
BuildPlan
Runtime
Recipe
RecipeExport
Adapter
Repair
Signing
AAPT2
Executor
Artifacts
Signature
Verify
Export
Report
Manifest
```

The pipeline is intentionally explicit: every important build transition can be validated and regression tested.

For a deeper overview see **[Architecture](docs/ARCHITECTURE.md)**.

---

## Development

```bash
python -m compileall -q anbe tests
python -m tests.run_ci
python -m tests.run_regression
python -m build
```

Recent compatibility work is covered by dedicated regression tests, including Android product-flavor handling, protobuf compatibility and Gradle command wiring. The full regression suite is expected to pass before compatibility changes are committed.

---

## Project principles

1. **Diagnose before mutating.**
2. **Prefer deterministic behavior over magic.**
3. **Treat build state as an explicit contract.**
4. **Never leak signing secrets into reports or source control.**
5. **Every architectural change needs regression coverage.**
6. **A successful Gradle command is not enough — verify the artifact.**
7. **Compatibility repairs should be targeted, safe and idempotent.**

---

## Roadmap

Near-term directions include broader native Android and Capacitor project coverage, additional Android project layouts and flavor configurations, broader compatibility repair coverage, stronger release readiness analysis, reproducible toolchain provisioning, additional host platforms and optional hosted build workflows.

See **[ROADMAP.md](docs/ROADMAP.md)**.

---

## Contributing

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md), [SUPPORT.md](SUPPORT.md), [SECURITY.md](SECURITY.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

Bug reports and feature requests can be submitted through GitHub Issues.

---

## License

ANBE is open-source software licensed under the **Apache License 2.0**. See [LICENSE](LICENSE).

---

<div align="center">

**Build Android. Verify the result. Ship with confidence.**

If ANBE is useful to you, consider giving the repository a ⭐.

</div>
