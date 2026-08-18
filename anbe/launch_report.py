#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

import hashlib
import json
import re


class LaunchReport:

    SCHEMA = "anbe.launch.report.v1"


    def android_root(self, ctx):

        configured = (
            ctx.recipe.get(
                "android_root"
            )
        )

        root = Path(
            ctx.path
        )

        if not configured:

            return root / "android"

        configured = Path(
            configured
        )

        if configured.is_absolute():

            return configured

        return root / configured


    def app_identity(self, ctx):

        android = self.android_root(
            ctx
        )

        gradle = (
            android
            /
            "app"
            /
            "build.gradle"
        )

        result = {
            "application_id": None,
            "namespace": None,
            "version_code": None,
            "version_name": None,
        }

        if not gradle.exists():

            return result

        text = gradle.read_text(
            errors="ignore"
        )

        patterns = {
            "application_id":
            r'applicationId\s+["\']([^"\']+)["\']',

            "namespace":
            r'namespace\s+["\']([^"\']+)["\']',

            "version_code":
            r'versionCode\s+([0-9]+)',

            "version_name":
            r'versionName\s+["\']([^"\']+)["\']',
        }

        for name, pattern in (
            patterns.items()
        ):

            match = re.search(
                pattern,
                text
            )

            if match:

                value = match.group(
                    1
                )

                if name == "version_code":

                    value = int(
                        value
                    )

                result[
                    name
                ] = value

        return result


    def file_sha256(self, path):

        digest = hashlib.sha256()

        with open(
            path,
            "rb"
        ) as handle:

            for block in iter(
                lambda:
                handle.read(
                    1024 * 1024
                ),
                b"",
            ):

                digest.update(
                    block
                )

        return digest.hexdigest()


    def artifact_info(self, ctx):

        if not ctx.exports:

            return None

        artifact = Path(
            ctx.exports[-1]
        )

        if not artifact.exists():

            return None

        return {
            "path":
            str(artifact),

            "filename":
            artifact.name,

            "format":
            artifact.suffix
            .lstrip(".")
            .lower(),

            "size_bytes":
            artifact.stat().st_size,

            "sha256":
            self.file_sha256(
                artifact
            ),
        }


    def signing_info(self, ctx):

        signature = (
            ctx.meta.get(
                "release_signature",
                {}
            )
        )

        signing = (
            ctx.meta.get(
                "release_signing",
                {}
            )
        )

        artifact_format = getattr(
            ctx,
            "artifact_format",
            "apk"
        )

        if artifact_format == "apk":

            status = (
                "verified"
                if signature.get(
                    "verified"
                )
                else "not_verified"
            )

        else:

            status = (
                "configured"
                if signing.get(
                    "configured"
                )
                else "unknown"
            )

        return {
            "status":
            status,

            "checked":
            signature.get(
                "checked",
                False
            ),

            "verified":
            signature.get(
                "verified"
            ),

            "certificate_sha256":
            signature.get(
                "certificate_sha256"
            ),

            "key_alias":
            signing.get(
                "key_alias"
            ),
        }


    def readiness(
        self,
        ctx,
        identity,
        artifact,
        signing,
    ):

        checks = []

        def add(
            name,
            passed,
            weight,
            detail=None,
        ):

            checks.append({
                "name":
                name,

                "passed":
                bool(passed),

                "weight":
                weight,

                "detail":
                detail,
            })

        verification = (
            ctx.meta.get(
                "verification",
                {}
            )
        )

        add(
            "release_mode",
            getattr(
                ctx,
                "build_mode",
                None
            ) == "release",
            10,
        )

        add(
            "artifact_created",
            artifact is not None,
            25,
        )

        add(
            "build_verified",
            verification.get(
                "success"
            ) is True,
            25,
        )

        add(
            "artifact_exported",
            bool(
                ctx.exports
            ),
            15,
        )

        add(
            "application_identity",
            bool(
                identity.get(
                    "application_id"
                )
            ),
            10,
            identity.get(
                "application_id"
            ),
        )

        add(
            "version_metadata",
            (
                identity.get(
                    "version_code"
                )
                is not None
                and
                bool(
                    identity.get(
                        "version_name"
                    )
                )
            ),
            5,
        )

        signing_ready = (
            signing.get(
                "status"
            )
            in (
                "verified",
                "configured",
            )
        )

        add(
            "release_signing",
            signing_ready,
            10,
            signing.get(
                "status"
            ),
        )

        score = sum(
            item[
                "weight"
            ]
            for item in checks
            if item[
                "passed"
            ]
        )

        if score >= 95:

            status = "READY"

        elif score >= 80:

            status = "REVIEW"

        else:

            status = "NOT_READY"

        return {
            "score":
            score,

            "max_score":
            100,

            "status":
            status,

            "checks":
            checks,
        }


    def create(self, ctx):

        identity = (
            self.app_identity(
                ctx
            )
        )

        artifact = (
            self.artifact_info(
                ctx
            )
        )

        signing = (
            self.signing_info(
                ctx
            )
        )

        readiness = (
            self.readiness(
                ctx,
                identity,
                artifact,
                signing,
            )
        )

        report = {
            "schema":
            self.SCHEMA,

            "created":
            datetime.now()
            .isoformat(),

            "product":
            "ANBE Launch",

            "project":
            str(
                ctx.path
            ),

            "build": {
                "mode":
                getattr(
                    ctx,
                    "build_mode",
                    None
                ),

                "format":
                getattr(
                    ctx,
                    "artifact_format",
                    None
                ),
            },

            "app":
            identity,

            "artifact":
            artifact,

            "signing":
            signing,

            "verification":
            ctx.meta.get(
                "verification",
                {}
            ),

            "readiness":
            readiness,
        }

        out = Path(
            "reports"
        )

        out.mkdir(
            parents=True,
            exist_ok=True
        )

        stamp = (
            datetime.now()
            .strftime(
                "%Y%m%d-%H%M%S"
            )
        )

        json_file = (
            out
            /
            (
                "launch-report-"
                +
                stamp
                +
                ".json"
            )
        )

        txt_file = (
            out
            /
            (
                "launch-report-"
                +
                stamp
                +
                ".txt"
            )
        )

        json_file.write_text(
            json.dumps(
                report,
                indent=2,
                ensure_ascii=False,
                default=str,
            )
            +
            "\n"
        )

        app = report[
            "app"
        ]

        art = report[
            "artifact"
        ] or {}

        lines = [
            "ANBE LAUNCH REPORT",
            "=" * 56,
            "",
            "Project: "
            + report[
                "project"
            ],
            "",
            "Application ID: "
            + str(
                app.get(
                    "application_id"
                )
            ),
            "Version: "
            + str(
                app.get(
                    "version_name"
                )
            )
            + " ("
            + str(
                app.get(
                    "version_code"
                )
            )
            + ")",
            "",
            "Build: "
            + str(
                report[
                    "build"
                ][
                    "mode"
                ]
            )
            + " / "
            + str(
                report[
                    "build"
                ][
                    "format"
                ]
            ),
            "",
            "Artifact: "
            + str(
                art.get(
                    "path"
                )
            ),
            "Size: "
            + str(
                art.get(
                    "size_bytes"
                )
            )
            + " bytes",
            "SHA-256: "
            + str(
                art.get(
                    "sha256"
                )
            ),
            "",
            "Signing: "
            + str(
                signing.get(
                    "status"
                )
            ),
            "Signer certificate SHA-256: "
            + str(
                signing.get(
                    "certificate_sha256"
                )
            ),
            "",
            "Release readiness: "
            + str(
                readiness[
                    "score"
                ]
            )
            + "/100 "
            + readiness[
                "status"
            ],
            "",
            "Checks:",
        ]

        for check in readiness[
            "checks"
        ]:

            lines.append(
                (
                    "[PASS] "
                    if check[
                        "passed"
                    ]
                    else "[FAIL] "
                )
                +
                check[
                    "name"
                ]
            )

        txt_file.write_text(
            "\n".join(
                lines
            )
            +
            "\n"
        )

        ctx.meta[
            "launch_report"
        ] = {
            "json":
            str(json_file),

            "text":
            str(txt_file),

            "score":
            readiness[
                "score"
            ],

            "status":
            readiness[
                "status"
            ],
        }

        return report
