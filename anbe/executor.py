#!/data/data/com.termux/files/usr/bin/python3

import os
from pathlib import Path

from .command_queue import CommandQueue
from .java_resolver import JavaResolver


class Executor:

    def android_root(self, ctx):

        root = Path(ctx.path)

        configured = ctx.recipe.get(
            "android_root"
        )

        if not configured:
            return root / "android"

        configured = Path(
            configured
        )

        if configured.is_absolute():
            return configured

        return root / configured


    def gradle_command(self, ctx):

        android = self.android_root(
            ctx
        )

        java = JavaResolver().resolve(
            android
        )

        aapt2 = (
            ctx.runtime.get("aapt2")
            or ctx.aapt2
        )

        if not aapt2:

            raise RuntimeError(
                "AAPT2 override unavailable before Gradle execution"
            )

        aapt2 = Path(aapt2)

        if not aapt2.exists():

            raise RuntimeError(
                "AAPT2 binary missing: "
                + str(aapt2)
            )

        command = (
            "./gradlew "
            f"-Pandroid.aapt2FromMavenOverride={aapt2} "
        )

        if java:

            command += (
                f"-Dorg.gradle.java.home={java} "
            )

        command += (
            "clean assembleDebug "
            "--no-daemon "
            "--stacktrace"
        )

        return command


    def execute(self, ctx):

        root = Path(ctx.path)

        android = self.android_root(
            ctx
        )

        java_home = os.environ.get(
            "JAVA_HOME",
            "/data/data/com.termux/files/usr/lib/jvm/"
            "java-21-openjdk"
        )

        os.environ[
            "JAVA_HOME"
        ] = java_home

        os.environ[
            "ORG_GRADLE_JAVA_INSTALLATIONS_PATHS"
        ] = java_home

        os.environ[
            "ORG_GRADLE_PROJECT_org.gradle.java.installations.paths"
        ] = java_home

        queue = CommandQueue()

        for step in ctx.recipe.get(
            "steps",
            []
        ):

            if step == "npm install":

                queue.add(
                    "npm install",
                    cwd=str(root)
                )

            elif step == "npm run build":

                queue.add(
                    "npm run build",
                    cwd=str(root)
                )

            elif step == "npx cap sync android":

                queue.add(
                    "npx cap sync android",
                    cwd=str(root)
                )

            elif step == "android prepare":

                ctx.info(
                    "Android preparation already handled"
                )

            elif step == "gradle assembleDebug":

                gradlew = (
                    android /
                    "gradlew"
                )

                if not gradlew.exists():

                    raise RuntimeError(
                        "Gradle wrapper missing: "
                        + str(gradlew)
                    )

                gradlew.chmod(
                    0o755
                )

                command = self.gradle_command(
                    ctx
                )

                ctx.info(
                    "Gradle AAPT2: "
                    + str(
                        ctx.runtime.get("aapt2")
                        or ctx.aapt2
                    )
                )

                queue.add(
                    command,
                    cwd=str(android)
                )

            else:

                ctx.warn(
                    "Unknown recipe step: "
                    + str(step)
                )

        ctx.execution = queue.execute()

        ctx.log(
            "Build executed"
        )

        return ctx
