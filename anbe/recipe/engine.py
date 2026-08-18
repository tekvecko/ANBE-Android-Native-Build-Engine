#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
import json

from .step import RecipeStep


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

            recipe[
                "steps"
            ].extend([
                RecipeStep.android_prepare(),
                RecipeStep.gradle(
                    "assembleDebug"
                ),
            ])

            if android_root == project:

                artifact_path = (
                    "app/build/outputs/apk/"
                    "debug/app-debug.apk"
                )

            else:

                artifact_path = (
                    str(
                        android_root.relative_to(
                            project
                        )
                    )
                    +
                    "/app/build/outputs/apk/"
                    "debug/app-debug.apk"
                )

            recipe[
                "artifact"
            ] = {
                "type":
                "apk",

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

        ctx.recipe = recipe

        ctx.log(
            "Dynamic recipe generated"
        )

        return ctx
