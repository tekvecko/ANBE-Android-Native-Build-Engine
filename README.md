<div align="center">

# ANBE

### Autonomous Android Native Build Engine

**From source project to verified Android release — locally, automatically, reproducibly.**

[![ANBE CI](https://github.com/tekvecko/ANBE-Android-Native-Build-Engine/actions/workflows/ci.yml/badge.svg)](https://github.com/tekvecko/ANBE-Android-Native-Build-Engine/actions/workflows/ci.yml)
[![Latest Release](https://img.shields.io/github/v/release/tekvecko/ANBE-Android-Native-Build-Engine?display_name=tag&sort=semver)](https://github.com/tekvecko/ANBE-Android-Native-Build-Engine/releases)
[![License](https://img.shields.io/github/license/tekvecko/ANBE-Android-Native-Build-Engine)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](pyproject.toml)
[![Platform](https://img.shields.io/badge/platform-Android%20%7C%20Termux%20%7C%20ARM64-green)](#supported-platform)

**[Quick Start](#quick-start) · [Launch](#anbe-launch) · [Architecture](docs/ARCHITECTURE.md) · [Roadmap](docs/ROADMAP.md) · [Contributing](CONTRIBUTING.md)**

</div>

---

## Why ANBE?

Building an Android application is often not a single command.

A real project may require:

- Node.js dependency installation
- frontend compilation
- Capacitor synchronization
- Android project repair
- Java / Gradle compatibility resolution
- AAPT2 discovery
- Gradle execution
- artifact discovery
- release signing
- signature validation
- APK/AAB export
- release verification

ANBE turns that chain into one deterministic pipeline.

```text
project
   │
   ▼
detect ──► analyze ──► plan ──► repair
                               │
                               ▼
                           toolchain
                               │
                               ▼
                             build
                               │
                               ▼
                       artifact discovery
                               │
                      ┌────────┴────────┐
                      ▼                 ▼
                     APK               AAB
                      │                 │
                      ▼                 ▼
                   verify            verify
                      │                 │
                      └────────┬────────┘
                               ▼
                           ANBE Launch
                               │
                               ▼
                      release-ready output
```

> **ANBE is not another Gradle wrapper.**
>
> It is an orchestration, diagnostics, repair and release layer around
> the Android build toolchain.

---

## The shortest version

```bash
anbe doctor ~/my-project
anbe launch ~/my-project
```

ANBE analyzes the project, prepares the toolchain, builds the application,
verifies the artifact and produces a release-readiness report.

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

---

## Features

### Build intelligence

- automatic project detection
- Capacitor-aware Android discovery
- structured build recipes
- dependency graph validation
- dependency-aware execution planning
- deterministic pipeline stages
- formal BuildContext contract

### Android toolchain

- Java / Gradle compatibility resolution
- Android preflight diagnostics
- ARM64 AAPT2 discovery
- Termux-aware Android execution
- Gradle wrapper preparation
- Android repair pipeline

### Release engineering

- debug APK builds
- release APK builds
- Android App Bundle (`.aab`) builds
- environment-based signing secrets
- APK signature verification
- signer certificate SHA-256 fingerprint
- artifact SHA-256 calculation
- release artifact export

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
- isolated Python package installation
- wheel / sdist distribution
- Apache-2.0 licensed

---

## Supported platform

### Stable path

| Component | Status |
|---|---|
| Android / Termux | ✅ Stable |
| ARM64 / aarch64 | ✅ Stable |
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

The current stable release is optimized for **Android + Termux + ARM64**.

ANBE is designed so broader host and framework support can be added without
replacing the core pipeline.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/tekvecko/ANBE-Android-Native-Build-Engine.git
cd ANBE-Android-Native-Build-Engine
```

Install ANBE:

```bash
./install.sh
```

Verify:

```bash
anbe --version
```

Expected output:

```text
ANBE 2.0.1
```

---

## Quick start

### 1. Diagnose

```bash
anbe doctor ~/my-project
```

The preflight checks the project, Android structure, Java, Gradle,
AAPT2 and other build requirements.

### 2. Build a debug APK

```bash
anbe build ~/my-project
```

### 3. Build a release APK

```bash
anbe release ~/my-project
```

### 4. Build an Android App Bundle

```bash
anbe release ~/my-project --aab
```

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

Launch performs the release build and produces release metadata such as:

- application ID
- version code
- version name
- artifact path
- artifact size
- artifact SHA-256
- release signing state
- signer certificate fingerprint for verified APKs
- release readiness score

---

## Secure release signing

ANBE does **not** store release passwords in the repository.

Configure signing through environment variables:

```bash
export ANBE_KEYSTORE="$HOME/.anbe/keys/release.jks"
export ANBE_KEYSTORE_PASSWORD="..."
export ANBE_KEY_ALIAS="..."
export ANBE_KEY_PASSWORD="..."
```

Then:

```bash
anbe launch ~/my-project
```

Keep the keystore outside project repositories and maintain a secure backup.

**Never commit signing credentials or production keystores.**

---

## Local-first by design

ANBE's current stable workflow runs locally.

Your source code does not need to be uploaded to a third-party build service
just to produce an Android artifact.

This makes ANBE useful for:

- independent developers
- local-first development
- Android-only environments
- Termux workflows
- AI-generated web applications moving to Android
- reproducible release automation
- build diagnostics and repair experiments

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

The pipeline is intentionally explicit: every important build transition can
be validated and regression tested.

For a deeper overview see **[Architecture](docs/ARCHITECTURE.md)**.

---

## Development

Compile the project:

```bash
python -m compileall -q anbe tests
```

Run portable tests:

```bash
python -m tests.run_ci
```

Run the full regression suite:

```bash
python -m tests.run_regression
```

Build Python distributions:

```bash
python -m build
```

---

## Project principles

ANBE development follows a few simple rules:

1. **Diagnose before mutating.**
2. **Prefer deterministic behavior over magic.**
3. **Treat build state as an explicit contract.**
4. **Never leak signing secrets into reports or source control.**
5. **Every architectural change needs regression coverage.**
6. **A successful Gradle command is not enough — verify the artifact.**

---

## Roadmap

Near-term directions include:

- broader Capacitor project coverage
- additional Android project layouts
- stronger release readiness analysis
- improved diagnostics and self-repair
- reproducible toolchain provisioning
- additional host platforms
- GitHub Actions integration
- optional hosted ANBE build service

See **[ROADMAP.md](docs/ROADMAP.md)**.

---

## Contributing

Contributions are welcome.

Start with:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SUPPORT.md](SUPPORT.md)
- [SECURITY.md](SECURITY.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

Bug reports and feature requests can be submitted through GitHub Issues.

---

## Security

Release signing is security-sensitive.

Please read **[SECURITY.md](SECURITY.md)** before working with production
signing material.

---

## License

ANBE is open-source software licensed under the
**Apache License 2.0**.

See [LICENSE](LICENSE).

---

<div align="center">

**Build Android. Verify the result. Ship with confidence.**

If ANBE is useful to you, consider giving the repository a ⭐.

</div>
