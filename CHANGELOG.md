# Changelog

## 2.1.0

Real-world Android compatibility and build UX release.

- flavored Android build detection and variant-aware Gradle task generation
- variant-aware APK artifact paths and repository-aware export naming
- Termux native `protoc` compatibility repair for incompatible Maven compiler binaries
- AndroidX core dependency compatibility repair
- safe Android launcher icon fallback
- progress reporting and heartbeat output for long-running builds
- incremental Gradle execution without an implicit `clean` before every build
- debug signing bridge skip and release-signing safety improvements
- successful on-device validation against Google's Now in Android `demoDebug` variant
- GitHub Pages project landing page and refreshed public repository presentation

## 2.0.1

Open-source stable release hardening.

- standard Python packaging
- relocatable CLI installation
- public README
- Apache-2.0 license
- security policy
- contribution guide
- synchronized version metadata

## 2.0.0

ANBE Launch MVP.

- `anbe launch`
- release readiness reports
- artifact SHA-256
- application identity and version metadata

## 1.9.1

- dedicated `anbe release` command

## 1.9.0

- secure release APK/AAB builder
- signing bridge
- APK signature verification

## 1.8.0

- dependency-aware execution planner

## 1.7.0

- recipe dependency graph

## 1.6.0

- structured recipe execution model

## 1.5.0

- CI
- formal BuildContext contract

## 1.4.0

- preflight diagnostics

## 1.3.0

- toolchain and artifact hardening

## 1.2.0

- regression suite

## 1.1.0

- unified pipeline orchestration

## 1.0.0

- first verified end-to-end Android APK build
