#!/data/data/com.termux/files/usr/bin/python3

import sys

from .orchestrator import Orchestrator
from .preflight import Preflight


BANNER = """
========================================
ANBE Autonomous Builder v1.0
========================================
"""


def usage():

    print(
        "Usage:"
    )

    print(
        "  anbe build <project>"
    )

    print(
        "  anbe doctor <project>"
    )


def main():

    args = sys.argv[
        1:
    ]

    if not args:

        usage()

        return 1

    command = args[
        0
    ]

    if command == "build":

        if len(args) < 2:

            usage()

            return 1

        project = args[
            1
        ]

        print(
            BANNER
        )

        Orchestrator().run(
            project
        )

        return 0

    if command == "doctor":

        if len(args) < 2:

            usage()

            return 1

        project = args[
            1
        ]

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
