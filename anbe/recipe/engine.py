#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
import json

from .step import RecipeStep
from .graph import RecipeGraph


class RecipeEngine:

    def generate(self, ctx):

        project = Path(
            ctx.path
        )

        recipe = {
            "schema":
            "anbe.recipe.dynamic.v3",

            "project":
            str(project),

            "steps":
            [],

            "android_root":
            None,

            "artifact":
            None,
        }

        # ---------------------------------------------
        # Node / frontend
        # ---------------------------------------------

        package_file = (
            project
            /
            "package.json"
        )

        if package_file.exists():

            recipe[
                "steps"
            ].append(
                RecipeStep.command(
                    "npm-install",
                    "npm install",
                )
            )

            try:

                package = json.loads(
                    package_file.read_text()
                )

            except Exception:

                package = {}

            scripts = package.get(
                "scripts",
                {}
            )

            if "build" in scripts:

                recipe[
                    "steps"
                ].append(
                    RecipeStep.command(
                        "npm-build",
                        "npm run build",
                        depends_on=[
                            "npm-install"
                        ],
                    )
                )

        # ---------------------------------------------
        # Capacitor
        # ---------------------------------------------

        capacitor_files = [
            (
                project
                /
                "capacitor.config.json"
            ),
            (
                project
                /
                "capacitor.config.ts"
            ),
        ]

        if any(
            p.exists()
            for p in capacitor_files
        ):

            recipe[
                "steps"
            ].append(
                RecipeStep.command(
                    "capacitor-sync-android",
                    "npx cap sync android",
                    depends_on=(
                        ["npm-build"]
                        if any(
                            step.get("id") == "npm-build"
                            for step in recipe["steps"]
                        )
                        else (
                            ["npm-install"]
                            if any(
                                step.get("id") == "npm-install"
                                for step in recipe["steps"]
                            )
                            else []
                        )
                    ),
                )
            )

        # ---------------------------------------------
        # Android project discovery
        # ---------------------------------------------

        android_candidates = [
            project / "android",
            project,
        ]

        android_root = None

        for candidate in android_candidates:

            indicators = [
                candidate / "gradlew",
                candidate / "build.gradle",
                candidate / "build.gradle.kts",
                candidate / "settings.gradle",
                candidate / "settings.gradle.kts",
            ]

            if any(
                item.exists()
                for item in indicators
            ):

                android_root = candidate
                break

        # ---------------------------------------------
        # Android build
        # ---------------------------------------------

        if android_root is not None:

            try:

                relative_android = (
                    android_root.relative_to(
                        project
                    )
                )

                android_root_value = str(
                    relative_android
                )

                if (
                    android_root_value
                    ==
                    "."
                ):

                    android_root_value = "."

            except ValueError:

                android_root_value = str(
                    android_root
                )

            recipe[
                "android_root"
            ] = android_root_value

            previous = []

            if any(
                step.get("id") == "capacitor-sync-android"
                for step in recipe["steps"]
            ):

                previous = [
                    "capacitor-sync-android"
                ]

            elif any(
                step.get("id") == "npm-build"
                for step in recipe["steps"]
            ):

                previous = [
                    "npm-build"
                ]

            elif any(
                step.get("id") == "npm-install"
                for step in recipe["steps"]
            ):

                previous = [
                    "npm-install"
                ]

            build_mode = getattr(
                ctx,
                "build_mode",
                "debug"
            )

            artifact_format = getattr(
                ctx,
                "artifact_format",
                "apk"
            )

            if build_mode == "release":

                gradle_task = (
                    "bundleRelease"
                    if artifact_format == "aab"
                    else "assembleRelease"
                )

            else:

                gradle_task = (
                    "assembleDebug"
                )

            recipe[
                "build"
            ] = {
                "mode":
                build_mode,

                "format":
                artifact_format,

                "gradle_task":
                gradle_task,
            }

            recipe[
                "steps"
            ].extend([
                RecipeStep.android_prepare(
                    depends_on=previous
                ),
                RecipeStep.gradle(
                    gradle_task,
                    depends_on=[
                        "android-prepare"
                    ],
                ),
            ])

            if build_mode == "debug":

                artifact_suffix = (
                    "app/build/outputs/apk/"
                    "debug/app-debug.apk"
                )

                artifact_type = "apk"

            elif artifact_format == "aab":

                artifact_suffix = (
                    "app/build/outputs/bundle/"
                    "release/app-release.aab"
                )

                artifact_type = "aab"

            else:

                from anbe.release_signing import ReleaseSigning

                signing = ReleaseSigning()

                if signing.configured():

                    artifact_suffix = (
                        "app/build/outputs/apk/"
                        "release/app-release.apk"
                    )

                else:

                    artifact_suffix = (
                        "app/build/outputs/apk/"
                        "release/app-release-unsigned.apk"
                    )

                artifact_type = "apk"

            if android_root == project:

                artifact_path = (
                    artifact_suffix
                )

            else:

                artifact_path = (
                    str(
                        android_root.relative_to(
                            project
                        )
                    )
                    +
                    "/"
                    +
                    artifact_suffix
                )

            recipe[
                "artifact"
            ] = {
                "type":
                artifact_type,

                "mode":
                build_mode,

                "path":
                artifact_path,
            }

        # Validate what the engine produced.
        recipe[
            "steps"
        ] = RecipeStep.normalize_all(
            recipe[
                "steps"
            ]
        )

        RecipeGraph.assert_valid(
            recipe[
                "steps"
            ]
        )

        recipe[
            "steps"
        ] = RecipeGraph.topological_sort(
            recipe[
                "steps"
            ]
        )

        ctx.recipe = recipe

        ctx.log(
            "Dynamic recipe generated"
        )

        return ctx
