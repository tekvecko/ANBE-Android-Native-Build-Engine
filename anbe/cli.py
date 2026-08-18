#!/data/data/com.termux/files/usr/bin/python3

import sys

from .orchestrator import Orchestrator
from .preflight import Preflight


def usage():

    print("Usage:")
    print("  anbe build <project>")
    print("  anbe build <project> --release")
    print("  anbe build <project> --release --aab")
    print("  anbe doctor <project>")


def main():

    args = sys.argv[1:]

    if not args:

        usage()
        return 1

    command = args[0]

    if command == "build":

        if len(args) < 2:

            usage()
            return 1

        project = args[1]

        flags = set(
            args[2:]
        )

        allowed = {
            "--release",
            "--apk",
            "--aab",
        }

        unknown = (
            flags
            -
            allowed
        )

        if unknown:

            print(
                "Unknown build option: "
                +
                ", ".join(
                    sorted(unknown)
                )
            )

            return 1

        build_mode = (
            "release"
            if "--release" in flags
            else "debug"
        )

        artifact_format = (
            "aab"
            if "--aab" in flags
            else "apk"
        )

        if (
            artifact_format == "aab"
            and
            build_mode != "release"
        ):

            print(
                "--aab requires --release"
            )

            return 1

        Orchestrator().run(
            project,
            build_mode=build_mode,
            artifact_format=artifact_format,
        )

        return 0

    if command == "doctor":

        if len(args) < 2:

            usage()
            return 1

        project = args[1]

        report = (
            Preflight()
            .run(
                project
            )
        )

        return (
            0
            if report["ready"]
            else 2
        )

    print(
        f"Unknown command: {command}"
    )

    usage()

    return 1


if __name__ == "__main__":

    raise SystemExit(
        main()
    )
