#!/data/data/com.termux/files/usr/bin/python3

import os
from pathlib import Path

from .command_queue import CommandQueue
from .java_resolver import JavaResolver
from .recipe.step import RecipeStep
from .recipe.graph import RecipeGraph


class Executor:

    def android_root(
        self,
        ctx
    ):

        root = Path(
            ctx.path
        )

        configured = ctx.recipe.get(
            "android_root"
        )

        if not configured:

            return (
                root
                /
                "android"
            )

        configured = Path(
            configured
        )

        if configured.is_absolute():

            return configured

        return (
            root
            /
            configured
        )


    def gradle_command(
        self,
        ctx,
        task="assembleDebug",
    ):

        android = self.android_root(
            ctx
        )

        java = JavaResolver().resolve(
            android
        )

        aapt2 = (
            ctx.runtime.get(
                "aapt2"
            )
            or
            ctx.aapt2
        )

        if not aapt2:

            raise RuntimeError(
                "AAPT2 override unavailable "
                "before Gradle execution"
            )

        aapt2 = Path(
            aapt2
        )

        if not aapt2.exists():

            raise RuntimeError(
                "AAPT2 binary missing: "
                +
                str(aapt2)
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
            "clean "
            +
            str(task)
            +
            " --no-daemon "
            "--stacktrace"
        )

        return command


    def step_cwd(
        self,
        step,
        root,
        android,
    ):

        selector = step.get(
            "cwd",
            "project"
        )

        if selector == "android":

            return android

        return root


    def execute(
        self,
        ctx
    ):

        root = Path(
            ctx.path
        )

        android = self.android_root(
            ctx
        )

        java_home = os.environ.get(
            "JAVA_HOME",
            "/data/data/com.termux/files/usr/"
            "lib/jvm/java-21-openjdk"
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

        steps = RecipeStep.normalize_all(
            ctx.recipe.get(
                "steps",
                []
            )
        )

        RecipeGraph.assert_valid(
            steps
        )

        steps = (
            RecipeGraph.topological_sort(
                steps
            )
        )

        # Execution remains sequential in v1.7,
        # but ordering is now derived from dependencies.
        ctx.recipe[
            "steps"
        ] = steps

        for step in steps:

            step_type = step[
                "type"
            ]

            if step_type == "command":

                command = step[
                    "command"
                ]

                cwd = self.step_cwd(
                    step,
                    root,
                    android,
                )

                queue.add(
                    command,
                    cwd=str(cwd)
                )

                continue

            if (
                step_type
                ==
                "android_prepare"
            ):

                ctx.info(
                    "Android preparation "
                    "already handled"
                )

                continue

            if step_type == "gradle":

                gradlew = (
                    android
                    /
                    "gradlew"
                )

                if not gradlew.exists():

                    raise RuntimeError(
                        "Gradle wrapper missing: "
                        +
                        str(gradlew)
                    )

                gradlew.chmod(
                    0o755
                )

                task = step.get(
                    "task",
                    "assembleDebug"
                )

                command = self.gradle_command(
                    ctx,
                    task=task,
                )

                ctx.info(
                    "Gradle AAPT2: "
                    +
                    str(
                        ctx.runtime.get(
                            "aapt2"
                        )
                        or
                        ctx.aapt2
                    )
                )

                queue.add(
                    command,
                    cwd=str(android)
                )

                continue

            raise RuntimeError(
                "Unsupported recipe step type: "
                +
                str(step_type)
            )

        ctx.execution = (
            queue.execute()
        )

        ctx.log(
            "Build executed"
        )

        return ctx
