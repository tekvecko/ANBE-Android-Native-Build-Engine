#!/data/data/com.termux/files/usr/bin/python3

import sys

from .orchestrator import Orchestrator
from .preflight import Preflight
from .release_signing import ReleaseSigning
from .launch_report import LaunchReport


def usage():

    print("Usage:")
    print("  anbe build <project>")
    print("  anbe build <project> --release")
    print("  anbe build <project> --release --aab")
    print("  anbe release <project>")
    print("  anbe release <project> --aab")
    print("  anbe launch <project>")
    print("  anbe launch <project> --aab")
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

    if command == "release":

        if len(args) < 2:

            usage()
            return 1

        project = args[1]

        flags = set(
            args[2:]
        )

        allowed = {
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
                "Unknown release option: "
                +
                ", ".join(
                    sorted(unknown)
                )
            )

            return 1

        artifact_format = (
            "aab"
            if "--aab" in flags
            else "apk"
        )

        signing = ReleaseSigning()

        status = signing.validate()

        if not status.get(
            "configured"
        ):

            print()
            print("ANBE RELEASE")
            print("=" * 48)
            print("[FAIL] Release signing is not configured")

            missing = status.get(
                "missing",
                []
            )

            if missing:
                print()
                print("Missing environment variables:")

                for name in missing:
                    print(" -", name)

            error = status.get(
                "error"
            )

            if error:
                print()
                print(error)

            print()
            print("Release aborted before build.")

            return 2

        Orchestrator().run(
            project,
            build_mode="release",
            artifact_format=artifact_format,
        )

        return 0


    if command == "launch":

        if len(args) < 2:

            usage()
            return 1

        project = args[1]

        flags = set(
            args[2:]
        )

        allowed = {
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
                "Unknown launch option: "
                +
                ", ".join(
                    sorted(unknown)
                )
            )

            return 1

        artifact_format = (
            "aab"
            if "--aab" in flags
            else "apk"
        )

        signing = ReleaseSigning()

        status = (
            signing.validate()
        )

        if not status.get(
            "configured"
        ):

            print()
            print("ANBE LAUNCH")
            print("=" * 48)
            print(
                "[FAIL] Release signing "
                "is not configured"
            )

            for name in status.get(
                "missing",
                []
            ):

                print(
                    " -",
                    name
                )

            error = status.get(
                "error"
            )

            if error:

                print(
                    error
                )

            return 2

        ctx = Orchestrator().run(
            project,
            build_mode="release",
            artifact_format=artifact_format,
        )

        report = (
            LaunchReport()
            .create(
                ctx
            )
        )

        readiness = report[
            "readiness"
        ]

        print()
        print("=" * 48)
        print("ANBE LAUNCH")
        print("=" * 48)

        print(
            "Application:",
            report[
                "app"
            ].get(
                "application_id"
            )
        )

        print(
            "Artifact:",
            (
                report[
                    "artifact"
                ] or {}
            ).get(
                "path"
            )
        )

        print(
            "Readiness:",
            str(
                readiness[
                    "score"
                ]
            )
            +
            "/100",
            readiness[
                "status"
            ]
        )

        launch_meta = ctx.meta[
            "launch_report"
        ]

        print(
            "JSON report:",
            launch_meta[
                "json"
            ]
        )

        print(
            "TXT report:",
            launch_meta[
                "text"
            ]
        )

        return (
            0
            if readiness[
                "status"
            ]
            ==
            "READY"
            else 3
        )


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
