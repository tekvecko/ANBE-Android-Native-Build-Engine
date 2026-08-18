#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


class GradleDoctor:

    def repair(self, ctx):

        root = Path(ctx.path)

        candidates = [
            root / "gradlew",
            root / "android" / "gradlew",
        ]

        gradlew = None

        for candidate in candidates:
            if candidate.exists():
                gradlew = candidate
                break

        if gradlew is None:
            ctx.warn("gradlew missing")
            ctx.runtime["gradlew"] = None
        else:
            gradlew.chmod(0o755)

            ctx.runtime["gradlew"] = str(gradlew)
            ctx.runtime["gradle_root"] = str(
                gradlew.parent
            )

            ctx.log(
                "gradlew ready: "
                + str(gradlew)
            )

        properties_candidates = [
            root / "android" / "gradle.properties",
            root / "gradle.properties",
        ]

        properties = None

        for candidate in properties_candidates:
            if candidate.exists():
                properties = candidate
                break

        if properties is None and gradlew is not None:
            properties = gradlew.parent / "gradle.properties"

        if properties is not None:

            properties.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            properties.touch(
                exist_ok=True
            )

            text = properties.read_text()

            if "org.gradle.jvmargs" not in text:
                text += (
                    "\n"
                    "org.gradle.jvmargs=-Xmx2048m\n"
                )

            aapt2 = (
                ctx.runtime.get("aapt2")
                or ctx.aapt2
            )

            if (
                aapt2
                and
                "android.aapt2FromMavenOverride"
                not in text
            ):
                text += (
                    "\n"
                    "android.aapt2FromMavenOverride="
                    + str(aapt2)
                    + "\n"
                )

                ctx.log(
                    "AAPT2 override written"
                )

            properties.write_text(text)

            ctx.runtime[
                "gradle_properties"
            ] = str(properties)

        return ctx
