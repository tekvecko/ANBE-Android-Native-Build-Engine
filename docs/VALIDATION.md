# ANBE Real-world Validation

ANBE is validated against real Android projects with substantially different build stacks.

The goal is not only to confirm that ANBE can build minimal templates, but to verify that its Android/Termux toolchain can handle large, modern and hybrid applications on-device.

---

## Validation matrix

| Project | Stack | Build | Tasks | ABI | Runtime result |
|---|---|---|---:|---|---|
| Google Now in Android | Kotlin, Compose, Hilt, KSP, Room, protobuf, Firebase | `:app:assembleDemoDebug` | 912 | ARM64 Android device | Installed and launched successfully |
| Electerm 5.2.0 | Capacitor, Node.js, JavaScript, C/C++, CMake, Android NDK, JNI, WebView | `assembleDebug` | 130 | `arm64-v8a` | Installed, launched, Node backend started, SSH session validated |

---

## Google Now in Android

ANBE successfully built Google's **Now in Android** reference application on an ARM64 Android device running Termux.

This validation covered a large modern Android project with multiple Gradle modules, Kotlin and Jetpack Compose, product flavors, Hilt, KSP, Room, protobuf, Firebase tooling, and variant-aware APK discovery.

Observed result:

```text
Task: :app:assembleDemoDebug
BUILD SUCCESSFUL
912 actionable tasks

APK:
app/build/outputs/apk/demo/debug/app-demo-debug.apk

Export:
/storage/emulated/0/Download/nowinandroid.apk
```

The resulting APK was installed and the application launched successfully on the Android device.

---

## Electerm 5.2.0

ANBE successfully built and ran **Electerm 5.2.0** entirely on an ARM64 Android device under Termux.

Its validated stack included Gradle, Capacitor, embedded Node.js, JavaScript frontend, native C/C++, CMake, Android NDK, JNI shared libraries, WebView, and SSH functionality.

Observed build result:

```text
Task: assembleDebug
BUILD SUCCESSFUL
130 actionable tasks

Package:
org.electerm.electerm

Launch activity:
org.electerm.electerm.MainActivity

ABI:
arm64-v8a
```

The resulting APK contained:

```text
lib/arm64-v8a/libc++_shared.so
lib/arm64-v8a/libcapacitor-nodejs.so
lib/arm64-v8a/liblog.so
lib/arm64-v8a/libnode.so
```

Runtime validation confirmed that the APK installed, `MainActivity` launched, `libnode.so` and `libcapacitor-nodejs.so` loaded, the embedded Node.js runtime started, the backend started on `127.0.0.1:5577`, the WebView frontend connected, the Electerm UI loaded, and an SSH session was successfully created against a Termux OpenSSH server.

Representative runtime output:

```text
NodejsPlugin: app start
NodejsPlugin: server runs on http://127.0.0.1:5577

GET / 200
GET /api/get-constants 200
```

---

## What these validations demonstrate

| Capability | Now in Android | Electerm |
|---|:---:|:---:|
| Large Gradle project | ✓ | ✓ |
| Multi-module build | ✓ | |
| Product flavors | ✓ | |
| Kotlin / Compose | ✓ | |
| KSP / Room | ✓ | |
| protobuf | ✓ | |
| Capacitor | | ✓ |
| Embedded Node.js | | ✓ |
| CMake | | ✓ |
| Android NDK | | ✓ |
| JNI native libraries | | ✓ |
| WebView frontend | | ✓ |
| Runtime backend | | ✓ |
| SSH client validation | | ✓ |
| Physical-device runtime test | ✓ | ✓ |

---

## Validation policy

A project should only be listed as runtime validated when all applicable stages have been confirmed: source preparation, dependency resolution, Android build, artifact production, ABI verification where applicable, physical-device installation, launch, and application-specific runtime validation.

---

## Current status

ANBE has now been validated against both a large modern native Android application and a complex hybrid Android application with an embedded Node.js and native C/C++ runtime.

## Reproducible evidence collector

ANBE includes `scripts/collect-validation-evidence.sh` for generating
Markdown evidence from a real Android build.

The collector records APK metadata, package and launch activity, SHA-256,
packaged ABIs, native shared libraries, Git revision and optional connected
device/runtime-log evidence.

Example:

```bash
scripts/collect-validation-evidence.sh \
  --project ~/anbe-demo-electerm/build/android/android \
  --apk ~/anbe-demo-electerm/build/android/android/app/build/outputs/apk/debug/app-debug.apk \
  --name "Electerm 5.2.0" \
  --gradle-task assembleDebug \
  --device 192.168.10.50:35325 \
  --runtime-log ~/electerm-runtime.log
```

Generated reports are stored by default under `docs/validation-runs/`.
