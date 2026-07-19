#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


HOME = Path.home()


RUNTIME = HOME / "ANBE-Runtime-Pack-v0.1"


CACHE = HOME / ".anbe"


REPORTS = CACHE / "reports"


EXPORTS = HOME / "storage" / "downloads"


# Compatibility aliases
# kept for existing modules


DOWNLOADS = EXPORTS


WORKSPACE = CACHE / "workspace"


BUILD_CACHE = CACHE / "build"


