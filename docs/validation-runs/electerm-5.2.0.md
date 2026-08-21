# Electerm 5.2.0 validation evidence

Generated: `2026-08-21T16:32:53+02:00`

## Build identity

| Field | Value |
|---|---|
| Project | `/data/data/com.termux/files/home/anbe-demo-electerm/build/android/android` |
| Git branch | `main` |
| Git revision | `3105be232121e301cdad4766357bd0addb0a2b61` |
| Gradle task | `assembleDebug` |
| APK | `/data/data/com.termux/files/home/anbe-demo-electerm/build/android/android/app/build/outputs/apk/debug/app-debug.apk` |
| APK size | `72MiB` |
| SHA-256 | `91f844358b23973b000225507b3ef399667b366adc436272aacbc99134f17240` |

## Android package

| Field | Value |
|---|---|
| Package | `org.electerm.electerm` |
| Launch activity | `org.electerm.electerm.MainActivity` |
| Version code | `1` |
| Version name | `1.0` |

## Packaged ABIs

- `arm64-v8a`

## Native libraries

```text
lib/arm64-v8a/libc++_shared.so
lib/arm64-v8a/libcapacitor-nodejs.so
lib/arm64-v8a/libnode.so
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

## Runtime validation

Runtime behavior was validated manually on a physical ARM64 Android device.

Observed result:

- package `org.electerm.electerm` installed successfully;
- `org.electerm.electerm.MainActivity` launched successfully;
- `libnode.so` loaded successfully;
- `libcapacitor-nodejs.so` loaded successfully;
- the embedded Node.js runtime started successfully;
- the Electerm backend reported `server runs on http://127.0.0.1:5577`;
- the WebView frontend connected to the local backend;
- an interactive SSH session was successfully opened against Termux OpenSSH.

The build artifact itself is reproducibly verified from the APK without
requiring ADB access.
