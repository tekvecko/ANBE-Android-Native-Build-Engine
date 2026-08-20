from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.context import BuildContext
from anbe.artifact.engine import ArtifactEngine

import anbe.artifact.engine as artifact_module


def test_artifact_detect_and_export():

    with TemporaryDirectory(
        prefix="anbe-artifact-test-"
    ) as tmp:

        root = Path(tmp)

        project = root / "project"

        apk = (
            project
            / "android"
            / "app"
            / "build"
            / "outputs"
            / "apk"
            / "debug"
            / "app-debug.apk"
        )

        apk.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        payload = b"ANBE-FAKE-APK"

        apk.write_bytes(
            payload
        )

        export_dir = (
            root
            / "downloads"
        )

        original_downloads = (
            artifact_module.DOWNLOADS
        )

        artifact_module.DOWNLOADS = (
            export_dir
        )

        try:

            ctx = BuildContext(
                project
            )

            engine = ArtifactEngine()

            engine.detect(
                ctx
            )

            assert len(
                ctx.artifacts
            ) == 1

            assert Path(
                ctx.artifacts[0]
            ) == apk

            engine.export(
                ctx
            )

            assert len(
                ctx.exports
            ) == 1

            exported = Path(
                ctx.exports[0]
            )

            expected_name = (
                engine.export_name(
                    ctx,
                    apk,
                )
            )

            assert exported == (
                export_dir
                /
                expected_name
            )

            assert exported.exists()

            assert exported.read_bytes() == (
                payload
            )

        finally:

            artifact_module.DOWNLOADS = (
                original_downloads
            )


if __name__ == "__main__":

    test_artifact_detect_and_export()

    print(
        "Artifact detect regression OK"
    )

    print(
        "Artifact export regression OK"
    )

    print(
        "ANBE artifact regression suite OK"
    )
