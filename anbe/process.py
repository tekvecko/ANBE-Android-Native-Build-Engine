#!/data/data/com.termux/files/usr/bin/python3

import subprocess
import time


class ProcessRunner:

    def run(
        self,
        cmd,
        cwd=None,
        check=True
    ):

        print("[>]", cmd)

        start = time.time()

        p = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            text=True,
            capture_output=True
        )

        elapsed = round(
            time.time() - start,
            2
        )

        result = {
            "command": cmd,
            "cwd": cwd,
            "returncode": p.returncode,
            "success": p.returncode == 0,
            "stdout": p.stdout,
            "stderr": p.stderr,
            "time": elapsed
        }

        if check and p.returncode != 0:
            raise RuntimeError(
                p.stderr if p.stderr else p.stdout
            )

        return result

