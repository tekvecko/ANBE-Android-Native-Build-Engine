#!/usr/bin/env python3

import subprocess
import time


def run(command, cwd=None):

    start = time.time()

    try:

        p = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            text=True,
            capture_output=True
        )

        return {
            "command": command,
            "cwd": str(cwd) if cwd else None,
            "returncode": p.returncode,
            "success": p.returncode == 0,
            "stdout": p.stdout,
            "stderr": p.stderr,
            "time": round(time.time()-start,3)
        }

    except Exception as e:

        return {
            "command": command,
            "success": False,
            "error": str(e),
            "time": round(time.time()-start,3)
        }
