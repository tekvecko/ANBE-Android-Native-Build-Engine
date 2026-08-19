# ANBE Roadmap

This roadmap describes direction rather than guaranteed delivery dates.

## Current: 2.x stable foundation

Completed:

- staged build pipeline
- formal BuildContext contract
- structured recipe model
- dependency graph
- dependency-aware execution planner
- Termux ARM64 Android toolchain support
- preflight diagnostics
- repair pipeline
- APK/AAB artifact discovery
- release signing bridge
- APK signature verification
- release readiness reports
- Python packaging
- CI and regression suites

## Next: ecosystem hardening

Priorities:

- test more real-world Capacitor projects
- improve error classification
- improve Android project discovery
- expand release verification
- improve runtime provisioning
- reduce assumptions tied to local paths
- add regression fixtures for more project layouts

## Future: wider platform support

Candidates:

- Linux host support
- macOS host support
- additional Android frameworks
- deeper Gradle project analysis
- configurable artifact targets
- CI-native operation

## Product direction

A future ANBE service may provide:

- repository import
- isolated remote builds
- build history
- artifact storage
- release diagnostics
- automated repair suggestions
- hosted Android build environments

The open-source engine remains the technological foundation.
