# Google Now in Android validation evidence

Generated: `2026-08-21T17:22:55+02:00`

## Build identity

| Field | Value |
|---|---|
| Project | `/data/data/com.termux/files/home/anbe-demo-nowinandroid` |
| Git branch | `main` |
| Git revision | `7d45eae4f8720a0c77f507712ba2437ff974b6ed` |
| Gradle task | `:app:assembleDemoDebug` |
| APK | `/data/data/com.termux/files/home/anbe-demo-nowinandroid/app/build/outputs/apk/demo/debug/app-demo-debug.apk` |
| APK size | `36MiB` |
| SHA-256 | `870534b59e80fe8432dab56ba8db6aae15d71bca53db8551d7b4f96a89ba4640` |

## Android package

| Field | Value |
|---|---|
| Package | `com.google.samples.apps.nowinandroid.demo.debug` |
| Launch activity | `com.google.samples.apps.nowinandroid.MainActivity` |
| Version code | `8` |
| Version name | `0.1.2` |

## Packaged ABIs

- `arm64-v8a`
- `armeabi-v7a`
- `x86`
- `x86_64`

## Native libraries

```text
lib/arm64-v8a/libandroidx.graphics.path.so
lib/arm64-v8a/libdatastore_shared_counter.so
lib/armeabi-v7a/libandroidx.graphics.path.so
lib/armeabi-v7a/libdatastore_shared_counter.so
lib/x86/libandroidx.graphics.path.so
lib/x86/libdatastore_shared_counter.so
lib/x86_64/libandroidx.graphics.path.so
lib/x86_64/libdatastore_shared_counter.so
```

## Device

| Field | Value |
|---|---|
| ADB serial | `not collected` |
| Device | `not collected` |
| Android API | `not collected` |
| Primary ABI | `not collected` |

## Runtime evidence

Runtime log was not supplied.

## Validation context

This project is Google's production-style **Now in Android** reference
application and represents a substantially larger native Android workload
than a minimal sample project.

The ANBE validation exercised:

- a large multi-module Kotlin/Compose codebase;
- product-flavor discovery and the `DemoDebug` variant;
- Hilt and KSP-based code generation;
- Room;
- protobuf tooling;
- Firebase-related build tooling;
- variant-aware APK discovery;
- Android/Termux host-tool compatibility handling;
- incremental Gradle build state preservation.

## Runtime validation

The generated APK was previously installed and launched successfully on a
physical Android device.

This report intentionally keeps the reproducible artifact evidence separate
from the previously observed runtime result, so the APK metadata, checksum,
ABI information and build identity can be regenerated without ADB access.
