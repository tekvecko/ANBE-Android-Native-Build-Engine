#!/data/data/com.termux/files/usr/bin/python3

import subprocess
import time


class ProcessRunner:

    HEARTBEAT_INTERVAL = 30


    def format_elapsed(
        self,
        seconds,
    ):

        seconds = int(
            seconds
        )

        minutes, seconds = divmod(
            seconds,
            60,
        )

        hours, minutes = divmod(
            minutes,
            60,
        )

        if hours:

            return (
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )

        return (
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )


    def run(
        self,
        cmd,
        cwd=None,
        check=True,
        heartbeat_interval=None,
    ):

        print(
            "[>]",
            cmd,
            flush=True,
        )

        interval = (
            heartbeat_interval
            if heartbeat_interval is not None
            else self.HEARTBEAT_INTERVAL
        )

        start = time.monotonic()

        process = subprocess.Popen(
            cmd,
            shell=True,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout = ""
        stderr = ""

        while True:

            try:

                stdout, stderr = (
                    process.communicate(
                        timeout=interval
                    )
                )

                break

            except subprocess.TimeoutExpired:

                elapsed = (
                    time.monotonic()
                    -
                    start
                )

                print(
                    "[…] Still working — "
                    +
                    self.format_elapsed(
                        elapsed
                    ),
                    flush=True,
                )

        elapsed = round(
            time.monotonic()
            -
            start,
            2,
        )

        result = {
            "command":
            cmd,

            "cwd":
            cwd,

            "returncode":
            process.returncode,

            "success":
            process.returncode == 0,

            "stdout":
            stdout,

            "stderr":
            stderr,

            "time":
            elapsed,
        }

        if (
            check
            and
            process.returncode != 0
        ):

            print(
                "\n=== COMMAND FAILED ==="
            )

            print(
                "CMD:",
                cmd
            )

            print(
                "CWD:",
                cwd
            )

            print(
                "\n--- STDOUT ---"
            )

            print(
                stdout
            )

            print(
                "\n--- STDERR ---"
            )

            print(
                stderr
            )

            raise RuntimeError(
                "command failed"
            )

        return result
