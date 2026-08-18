from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from anbe.context import BuildContext
from anbe.release_signature_verifier import (
    ReleaseSignatureVerifier,
)


class FakeProcess:

    def __init__(
        self,
        returncode=0,
        stdout="",
        stderr="",
    ):

        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def release_context(
    root
):

    ctx = BuildContext(
        root
    )

    ctx.build_mode = "release"
    ctx.artifact_format = "apk"

    apk = (
        root
        /
        "app-release.apk"
    )

    apk.write_bytes(
        b"APK"
    )

    ctx.artifacts.append(
        apk
    )

    return ctx


def test_signature_verifier_success():

    with TemporaryDirectory(
        prefix="anbe-signature-"
    ) as tmp:

        root = Path(
            tmp
        )

        ctx = release_context(
            root
        )

        output = '''
Verifies
V2 Signer: certificate SHA-256 digest: a209b3774d1b97723a5528f6767865771e87ca563e0a7d69e0b5d195b3038898
'''

        with (
            patch(
                "anbe.release_signature_verifier.shutil.which",
                return_value="/usr/bin/apksigner",
            ),
            patch(
                "anbe.release_signature_verifier.subprocess.run",
                return_value=FakeProcess(
                    returncode=0,
                    stdout=output,
                ),
            )
        ):

            ReleaseSignatureVerifier().verify(
                ctx
            )

        result = ctx.meta[
            "release_signature"
        ]

        assert result[
            "verified"
        ] is True

        assert result[
            "certificate_sha256"
        ] == (
            "a209b3774d1b97723a5528f6767865771"
            "e87ca563e0a7d69e0b5d195b3038898"
        )


def test_signature_verifier_failure():

    with TemporaryDirectory(
        prefix="anbe-signature-fail-"
    ) as tmp:

        root = Path(
            tmp
        )

        ctx = release_context(
            root
        )

        with (
            patch(
                "anbe.release_signature_verifier.shutil.which",
                return_value="/usr/bin/apksigner",
            ),
            patch(
                "anbe.release_signature_verifier.subprocess.run",
                return_value=FakeProcess(
                    returncode=1,
                    stderr="DOES NOT VERIFY",
                ),
            )
        ):

            try:

                ReleaseSignatureVerifier().verify(
                    ctx
                )

            except RuntimeError:

                assert (
                    ctx.meta[
                        "release_signature"
                    ][
                        "verified"
                    ]
                    is False
                )

                return

        raise AssertionError(
            "Invalid release APK accepted"
        )


def test_signature_verifier_debug_skip():

    with TemporaryDirectory(
        prefix="anbe-signature-debug-"
    ) as tmp:

        root = Path(
            tmp
        )

        ctx = BuildContext(
            root
        )

        ReleaseSignatureVerifier().verify(
            ctx
        )

        assert (
            ctx.meta[
                "release_signature"
            ][
                "reason"
            ]
            ==
            "not_release"
        )


def test_signature_verifier_aab_skip():

    with TemporaryDirectory(
        prefix="anbe-signature-aab-"
    ) as tmp:

        root = Path(
            tmp
        )

        ctx = BuildContext(
            root
        )

        ctx.build_mode = "release"
        ctx.artifact_format = "aab"

        ReleaseSignatureVerifier().verify(
            ctx
        )

        assert (
            ctx.meta[
                "release_signature"
            ][
                "reason"
            ]
            ==
            "not_apk"
        )


if __name__ == "__main__":

    test_signature_verifier_success()
    print(
        "Release signature verification OK"
    )

    test_signature_verifier_failure()
    print(
        "Invalid signature rejection OK"
    )

    test_signature_verifier_debug_skip()
    print(
        "Debug signature skip OK"
    )

    test_signature_verifier_aab_skip()
    print(
        "AAB signature skip OK"
    )
