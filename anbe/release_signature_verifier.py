#!/usr/bin/env python3

from pathlib import Path
import re
import shutil
import subprocess


class ReleaseSignatureVerifier:

    SHA256_RE = re.compile(
        r"certificate SHA-256 digest:\s*([0-9a-fA-F]+)"
    )


    def verify(self, ctx):

        mode = getattr(
            ctx,
            "build_mode",
            "debug"
        )

        artifact_format = getattr(
            ctx,
            "artifact_format",
            "apk"
        )

        result = {
            "checked": False,
            "verified": None,
            "tool": None,
            "artifact": None,
            "certificate_sha256": None,
            "reason": None,
        }

        ctx.meta[
            "release_signature"
        ] = result

        if mode != "release":

            result["reason"] = (
                "not_release"
            )

            return ctx

        if artifact_format != "apk":

            result["reason"] = (
                "not_apk"
            )

            return ctx

        apk = None

        for artifact in ctx.artifacts:

            candidate = Path(
                artifact
            )

            if (
                candidate.suffix.lower()
                ==
                ".apk"
            ):

                apk = candidate
                break

        if apk is None:

            raise RuntimeError(
                "Release APK signature verification "
                "requested but no APK artifact exists"
            )

        result[
            "artifact"
        ] = str(
            apk
        )

        apksigner = shutil.which(
            "apksigner"
        )

        if not apksigner:

            result[
                "reason"
            ] = "apksigner_unavailable"

            ctx.warn(
                "apksigner unavailable; "
                "release signature verification skipped"
            )

            return ctx

        result[
            "tool"
        ] = apksigner

        proc = subprocess.run(
            [
                apksigner,
                "verify",
                "--verbose",
                "--print-certs",
                str(apk),
            ],
            capture_output=True,
            text=True,
        )

        output = (
            proc.stdout
            +
            "\n"
            +
            proc.stderr
        )

        result[
            "checked"
        ] = True

        if proc.returncode != 0:

            result[
                "verified"
            ] = False

            result[
                "reason"
            ] = "verification_failed"

            raise RuntimeError(
                "Release APK signature verification failed"
            )

        match = (
            self.SHA256_RE.search(
                output
            )
        )

        result[
            "verified"
        ] = True

        result[
            "reason"
        ] = "verified"

        if match:

            result[
                "certificate_sha256"
            ] = (
                match.group(1)
                .lower()
            )

        ctx.log(
            "Release APK signature verified"
        )

        if result[
            "certificate_sha256"
        ]:

            ctx.info(
                "Signer certificate SHA-256: "
                +
                result[
                    "certificate_sha256"
                ]
            )

        return ctx
