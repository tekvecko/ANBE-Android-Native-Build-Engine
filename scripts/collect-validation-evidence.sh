#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/collect-validation-evidence.sh \
    --project /path/to/android/project \
    --apk /path/to/app.apk \
    --name "Project Name" \
    [--gradle-task assembleDebug] \
    [--device SERIAL] \
    [--runtime-log /path/to/logcat.txt] \
    [--output docs/validation-runs/project.md] \
    [--json-output docs/validation-runs/project.json]

The script collects reproducible Android validation evidence:
- Git revision when available
- APK metadata
- package name
- launchable activity
- version code/name
- APK size and SHA-256
- packaged Android ABIs
- packaged native .so libraries
- optional connected-device metadata
- optional runtime log highlights
USAGE
}

PROJECT=""
APK=""
NAME=""
GRADLE_TASK="assembleDebug"
DEVICE=""
RUNTIME_LOG=""
OUTPUT=""
JSON_OUTPUT=""

while (($#)); do
  case "$1" in
    --project)
      PROJECT="${2:?missing value for --project}"
      shift 2
      ;;
    --apk)
      APK="${2:?missing value for --apk}"
      shift 2
      ;;
    --name)
      NAME="${2:?missing value for --name}"
      shift 2
      ;;
    --gradle-task)
      GRADLE_TASK="${2:?missing value for --gradle-task}"
      shift 2
      ;;
    --device)
      DEVICE="${2:?missing value for --device}"
      shift 2
      ;;
    --runtime-log)
      RUNTIME_LOG="${2:?missing value for --runtime-log}"
      shift 2
      ;;
    --output)
      OUTPUT="${2:?missing value for --output}"
      shift 2
      ;;
    --json-output)
      JSON_OUTPUT="${2:?missing value for --json-output}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[FAIL] Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -n "$PROJECT" ]] || { echo "[FAIL] --project is required" >&2; exit 2; }
[[ -n "$APK" ]] || { echo "[FAIL] --apk is required" >&2; exit 2; }
[[ -n "$NAME" ]] || { echo "[FAIL] --name is required" >&2; exit 2; }

PROJECT="$(cd "$PROJECT" && pwd)"
APK="$(cd "$(dirname "$APK")" && pwd)/$(basename "$APK")"

[[ -f "$APK" ]] || { echo "[FAIL] APK not found: $APK" >&2; exit 1; }

command -v aapt >/dev/null 2>&1 || {
  echo "[FAIL] aapt is required in PATH" >&2
  exit 1
}

command -v unzip >/dev/null 2>&1 || {
  echo "[FAIL] unzip is required in PATH" >&2
  exit 1
}

slug="$(
  printf '%s' "$NAME" |
    tr '[:upper:]' '[:lower:]' |
    sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g'
)"

if [[ -z "$OUTPUT" ]]; then
  OUTPUT="docs/validation-runs/${slug}.md"
fi

if [[ -z "$JSON_OUTPUT" ]]; then
  if [[ "$OUTPUT" == *.md ]]; then
    JSON_OUTPUT="${OUTPUT%.md}.json"
  else
    JSON_OUTPUT="${OUTPUT}.json"
  fi
fi

mkdir -p "$(dirname "$OUTPUT")"
mkdir -p "$(dirname "$JSON_OUTPUT")"

badging="$(aapt dump badging "$APK" 2>/dev/null || true)"
package_line="$(printf '%s\n' "$badging" | grep '^package:' | head -1 || true)"
launch_line="$(printf '%s\n' "$badging" | grep '^launchable-activity:' | head -1 || true)"

extract_attr() {
  local line="$1"
  local key="$2"

  printf '%s\n' "$line" |
    grep -oE "(^|[[:space:]])${key}='[^']*'" |
    head -1 |
    sed -E "s/^[[:space:]]*${key}='([^']*)'$/\\1/" ||
    true
}

package_name="$(extract_attr "$package_line" "name")"
version_code="$(extract_attr "$package_line" "versionCode")"
version_name="$(extract_attr "$package_line" "versionName")"
launch_activity="$(extract_attr "$launch_line" "name")"

apk_size_bytes="$(wc -c < "$APK" | tr -d ' ')"
apk_size_human="$(
  if command -v numfmt >/dev/null 2>&1; then
    numfmt --to=iec-i --suffix=B "$apk_size_bytes"
  else
    printf '%s bytes' "$apk_size_bytes"
  fi
)"

if command -v sha256sum >/dev/null 2>&1; then
  apk_sha256="$(sha256sum "$APK" | awk '{print $1}')"
else
  apk_sha256="unavailable"
fi

mapfile -t native_libs < <(
  unzip -Z1 "$APK" 2>/dev/null |
    grep -E '^lib/[^/]+/[^/]+\.so$' |
    sort -u || true
)

mapfile -t abis < <(
  printf '%s\n' "${native_libs[@]:-}" |
    sed -n 's#^lib/\([^/]*\)/.*#\1#p' |
    sort -u
)

git_revision="not available"
git_branch="not available"

if git -C "$PROJECT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git_revision="$(git -C "$PROJECT" rev-parse HEAD)"
  git_branch="$(git -C "$PROJECT" branch --show-current || true)"
  [[ -n "$git_branch" ]] || git_branch="detached HEAD"
fi

device_summary="not collected"
device_sdk="not collected"
device_abi="not collected"

if [[ -n "$DEVICE" ]]; then
  command -v adb >/dev/null 2>&1 || {
    echo "[FAIL] adb is required when --device is used" >&2
    exit 1
  }

  adb -s "$DEVICE" get-state >/dev/null

  manufacturer="$(adb -s "$DEVICE" shell getprop ro.product.manufacturer | tr -d '\r')"
  model="$(adb -s "$DEVICE" shell getprop ro.product.model | tr -d '\r')"
  device_sdk="$(adb -s "$DEVICE" shell getprop ro.build.version.sdk | tr -d '\r')"
  device_abi="$(adb -s "$DEVICE" shell getprop ro.product.cpu.abi | tr -d '\r')"
  device_summary="${manufacturer} ${model}"
fi

runtime_section="Runtime log was not supplied."

if [[ -n "$RUNTIME_LOG" ]]; then
  [[ -f "$RUNTIME_LOG" ]] || {
    echo "[FAIL] runtime log not found: $RUNTIME_LOG" >&2
    exit 1
  }

  highlights="$(
    grep -E \
      'BUILD SUCCESSFUL|NodejsPlugin|libnode|libcapacitor-nodejs|server runs on|GET / 200|FATAL EXCEPTION|AndroidRuntime|ERR_MODULE_NOT_FOUND|SSH|ssh' \
      "$RUNTIME_LOG" |
      tail -120 || true
  )"

  if [[ -n "$highlights" ]]; then
    runtime_section="$(cat <<RUNTIME
\`\`\`text
$highlights
\`\`\`
RUNTIME
)"
  else
    runtime_section="No matching runtime highlights were found in the supplied log."
  fi
fi

{
  printf '# %s validation evidence\n\n' "$NAME"
  printf 'Generated: `%s`\n\n' "$(date -Iseconds)"

  printf '## Build identity\n\n'
  printf '| Field | Value |\n'
  printf '|---|---|\n'
  printf '| Project | `%s` |\n' "$PROJECT"
  printf '| Git branch | `%s` |\n' "$git_branch"
  printf '| Git revision | `%s` |\n' "$git_revision"
  printf '| Gradle task | `%s` |\n' "$GRADLE_TASK"
  printf '| APK | `%s` |\n' "$APK"
  printf '| APK size | `%s` |\n' "$apk_size_human"
  printf '| SHA-256 | `%s` |\n' "$apk_sha256"
  printf '\n'

  printf '## Android package\n\n'
  printf '| Field | Value |\n'
  printf '|---|---|\n'
  printf '| Package | `%s` |\n' "${package_name:-not detected}"
  printf '| Launch activity | `%s` |\n' "${launch_activity:-not detected}"
  printf '| Version code | `%s` |\n' "${version_code:-not detected}"
  printf '| Version name | `%s` |\n' "${version_name:-not detected}"
  printf '\n'

  printf '## Packaged ABIs\n\n'
  if ((${#abis[@]})); then
    for abi in "${abis[@]}"; do
      printf -- '- `%s`\n' "$abi"
    done
  else
    printf 'No native ABI directories detected in the APK.\n'
  fi
  printf '\n'

  printf '## Native libraries\n\n'
  if ((${#native_libs[@]})); then
    printf '```text\n'
    printf '%s\n' "${native_libs[@]}"
    printf '```\n'
  else
    printf 'No packaged `.so` libraries detected.\n'
  fi
  printf '\n'

  printf '## Device\n\n'
  printf '| Field | Value |\n'
  printf '|---|---|\n'
  printf '| ADB serial | `%s` |\n' "${DEVICE:-not collected}"
  printf '| Device | `%s` |\n' "$device_summary"
  printf '| Android API | `%s` |\n' "$device_sdk"
  printf '| Primary ABI | `%s` |\n' "$device_abi"
  printf '\n'

  printf '## Runtime evidence\n\n'
  printf '%s\n' "$runtime_section"
} > "$OUTPUT"


echo
echo "===== WRITE JSON EVIDENCE ====="

export ANBE_JSON_NAME="$NAME"
export ANBE_JSON_PROJECT="$PROJECT"
export ANBE_JSON_APK="$APK"
export ANBE_JSON_GRADLE_TASK="$GRADLE_TASK"
export ANBE_JSON_OUTPUT="$OUTPUT"
export ANBE_JSON_JSON_OUTPUT="$JSON_OUTPUT"
export ANBE_JSON_PACKAGE="${package_name:-}"
export ANBE_JSON_LAUNCH_ACTIVITY="${launch_activity:-}"
export ANBE_JSON_VERSION_CODE="${version_code:-}"
export ANBE_JSON_VERSION_NAME="${version_name:-}"
export ANBE_JSON_APK_SIZE_BYTES="$apk_size_bytes"
export ANBE_JSON_APK_SIZE_HUMAN="$apk_size_human"
export ANBE_JSON_APK_SHA256="$apk_sha256"
export ANBE_JSON_GIT_BRANCH="$git_branch"
export ANBE_JSON_GIT_REVISION="$git_revision"
export ANBE_JSON_DEVICE_SERIAL="${DEVICE:-}"
export ANBE_JSON_DEVICE_SUMMARY="$device_summary"
export ANBE_JSON_DEVICE_SDK="$device_sdk"
export ANBE_JSON_DEVICE_ABI="$device_abi"
export ANBE_JSON_ABIS="$(printf '%s\n' "${abis[@]:-}")"
export ANBE_JSON_NATIVE_LIBS="$(printf '%s\n' "${native_libs[@]:-}")"

python - <<'PYJSON'
import json
import os
from datetime import datetime

def env(name, default=""):
    return os.environ.get(name, default)

def lines(name):
    return [line for line in env(name).splitlines() if line]

payload = {
    "schema_version": 1,
    "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    "name": env("ANBE_JSON_NAME"),
    "build": {
        "project": env("ANBE_JSON_PROJECT"),
        "git_branch": env("ANBE_JSON_GIT_BRANCH"),
        "git_revision": env("ANBE_JSON_GIT_REVISION"),
        "gradle_task": env("ANBE_JSON_GRADLE_TASK"),
    },
    "apk": {
        "path": env("ANBE_JSON_APK"),
        "size_bytes": int(env("ANBE_JSON_APK_SIZE_BYTES", "0")),
        "size_human": env("ANBE_JSON_APK_SIZE_HUMAN"),
        "sha256": env("ANBE_JSON_APK_SHA256"),
        "abis": lines("ANBE_JSON_ABIS"),
        "native_libraries": lines("ANBE_JSON_NATIVE_LIBS"),
    },
    "android": {
        "package": env("ANBE_JSON_PACKAGE"),
        "launch_activity": env("ANBE_JSON_LAUNCH_ACTIVITY"),
        "version_code": env("ANBE_JSON_VERSION_CODE"),
        "version_name": env("ANBE_JSON_VERSION_NAME"),
    },
    "device": {
        "adb_serial": env("ANBE_JSON_DEVICE_SERIAL"),
        "summary": env("ANBE_JSON_DEVICE_SUMMARY"),
        "android_api": env("ANBE_JSON_DEVICE_SDK"),
        "primary_abi": env("ANBE_JSON_DEVICE_ABI"),
    },
    "reports": {
        "markdown": env("ANBE_JSON_OUTPUT"),
        "json": env("ANBE_JSON_JSON_OUTPUT"),
    },
}

with open(env("ANBE_JSON_JSON_OUTPUT"), "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2, ensure_ascii=False)
    f.write("\n")
PYJSON

echo "[OK] JSON evidence written to: $JSON_OUTPUT"

echo "[OK] Validation evidence written to: $OUTPUT"
