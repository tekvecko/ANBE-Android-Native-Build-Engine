#!/data/data/com.termux/files/usr/bin/python3

import os
from pathlib import Path

from .command_queue import CommandQueue
from .java_resolver import JavaResolver
from .recipe.step import RecipeStep
from .recipe.graph import RecipeGraph
from .execution_planner import ExecutionPlanner
from .release_signing import ReleaseSigning


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

        java_resolver = JavaResolver()

        java = java_resolver.resolve(
            android
        )

        if not java:

            gradle_version = (
                java_resolver.gradle_version(
                    android
                )
            )

            required_java = (
                java_resolver.required_java(
                    android
                )
            )

            maximum_java = (
                java_resolver.gradle_runtime_max_java(
                    android
                )
            )

            message = (
                "Compatible Java runtime unavailable"
            )

            if gradle_version:

                message += (
                    " for Gradle "
                    +
                    str(
                        gradle_version
                    )
                )

            message += (
                "; project Java target: "
                +
                str(
                    required_java
                )
            )

            if maximum_java is not None:

                message += (
                    "; maximum Gradle runtime Java: "
                    +
                    str(
                        maximum_java
                    )
                )

            raise RuntimeError(
                message
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

        release = (
            str(task).lower()
            .endswith("release")
        )

        if release:

            signing = ReleaseSigning()

            status = (
                signing.validate()
            )

            if status.get(
                "configured"
            ):

                for name, value in (
                    signing
                    .gradle_environment()
                    .items()
                ):

                    os.environ[
                        name
                    ] = value

                ctx.meta[
                    "release_signing"
                ] = {
                    "configured":
                    True,

                    "keystore":
                    status.get(
                        "keystore"
                    ),

                    "key_alias":
                    status.get(
                        "key_alias"
                    ),
                }

            else:

                ctx.meta[
                    "release_signing"
                ] = status

                ctx.warn(
                    "Release signing credentials "
                    "not fully configured"
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


    def progress_percent(
        self,
        completed,
        total,
    ):

        if total <= 0:

            return 100

        value = int(
            round(
                (
                    completed
                    /
                    total
                )
                *
                100
            )
        )

        return max(
            0,
            min(
                100,
                value,
            ),
        )


    def report_progress(
        self,
        ctx,
        completed,
        total,
        step=None,
    ):

        percent = self.progress_percent(
            completed,
            total,
        )

        message = (
            "Progress: "
            +
            str(percent)
            +
            "%"
        )

        if step:

            step_id = step.get(
                "id"
            )

            if step_id:

                message += (
                    " ["
                    +
                    str(step_id)
                    +
                    "]"
                )

        ctx.info(
            message
        )


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

        planner = ExecutionPlanner()

        execution_plan = (
            planner.plan(
                steps
            )
        )

        steps = (
            planner.ordered_steps(
                steps
            )
        )

        # v1.8 execution is deliberately sequential.
        # The planner now exposes dependency waves so
        # a later concurrent runner can safely consume them.
        ctx.recipe[
            "steps"
        ] = steps

        ctx.meta[
            "execution_plan"
        ] = execution_plan

        ctx.info(
            "Execution plan: "
            +
            str(
                execution_plan[
                    "wave_count"
                ]
            )
            +
            " wave(s), "
            +
            str(
                execution_plan[
                    "step_count"
                ]
            )
            +
            " step(s)"
        )

        total_steps = len(
            steps
        )

        completed_steps = 0

        self.report_progress(
            ctx,
            completed_steps,
            total_steps,
        )

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

                completed_steps += 1

                self.report_progress(
                    ctx,
                    completed_steps,
                    total_steps,
                    step=step,
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

                completed_steps += 1

                self.report_progress(
                    ctx,
                    completed_steps,
                    total_steps,
                    step=step,
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

                completed_steps += 1

                self.report_progress(
                    ctx,
                    completed_steps,
                    total_steps,
                    step=step,
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
