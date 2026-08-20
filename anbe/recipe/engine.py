#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
import json

from .step import RecipeStep
from .graph import RecipeGraph
from anbe.package_manager import PackageManagerResolver


class RecipeEngine:

    def android_flavors(
        self,
        android_root,
    ):

        root = Path(
            android_root
        )

        names = []

        patterns = (
            r'register\(\s*["\']([A-Za-z0-9_-]+)["\']\s*\)',
            r'create\(\s*["\']([A-Za-z0-9_-]+)["\']\s*\)',
            r'productFlavors\s*\{',
        )

        files = []

        for pattern in (
            "*.gradle",
            "*.gradle.kts",
            "*.kt",
            "*.kts",
        ):

            files.extend(
                root.rglob(
                    pattern
                )
            )

        for path in files:

            try:

                text = path.read_text(
                    errors="ignore"
                )

            except Exception:

                continue

            if (
                "productFlavors"
                not in text
                and
                "Flavor"
                not in text
            ):

                continue

            for regex in patterns[:2]:

                import re

                for match in re.finditer(
                    regex,
                    text,
                ):

                    value = match.group(1)

                    if (
                        value
                        not in names
                    ):

                        names.append(
                            value
                        )

            if (
                "enum class NiaFlavor"
                in text
            ):

                import re

                block = re.search(
                    r'enum class NiaFlavor[^{]*\{([^}]+)\}',
                    text,
                    re.DOTALL,
                )

                if block:

                    for match in re.finditer(
                        r'^\s*([A-Za-z][A-Za-z0-9_]*)\s*\(',
                        block.group(1),
                        re.MULTILINE,
                    ):

                        value = match.group(1)

                        if (
                            value
                            not in names
                        ):

                            names.append(
                                value
                            )

        return names


    def preferred_android_flavor(
        self,
        android_root,
    ):

        flavors = self.android_flavors(
            android_root
        )

        if "demo" in flavors:

            return "demo"

        return None


    def variant_name(
        self,
        flavor,
        build_mode,
    ):

        suffix = (
            "Release"
            if build_mode == "release"
            else "Debug"
        )

        if not flavor:

            return suffix

        return (
            str(flavor)[:1].upper()
            +
            str(flavor)[1:]
            +
            suffix
        )


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

            try:

                package = json.loads(
                    package_file.read_text()
                )

            except Exception:

                package = {}

            package_manager_resolver = (
                PackageManagerResolver()
            )

            package_manager_info = (
                package_manager_resolver.detect(
                    project
                )
            )

            package_manager = (
                package_manager_info[
                    "name"
                ]
            )

            package_commands = (
                package_manager_resolver.commands(
                    project
                )
            )

            install_command = (
                package_commands[
                    "install"
                ]
            )

            build_command = (
                package_commands[
                    "build"
                ]
            )

            capacitor_command = (
                package_commands[
                    "capacitor"
                ]
            )

            recipe[
                "package_manager"
            ] = package_manager

            recipe[
                "package_manager_info"
            ] = package_manager_info

            recipe[
                "steps"
            ].append(
                RecipeStep.command(
                    "npm-install",
                    install_command,
                )
            )

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
                        build_command,
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
                    (
                        capacitor_command
                        if package_file.exists()
                        else "npx cap sync android"
                    ),
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

            flavor = (
                self.preferred_android_flavor(
                    android_root
                )
            )

            variant = self.variant_name(
                flavor,
                build_mode,
            )

            if build_mode == "release":

                gradle_task = (
                    (
                        "bundle"
                        +
                        variant
                    )
                    if artifact_format == "aab"
                    else (
                        "assemble"
                        +
                        variant
                    )
                )

            else:

                gradle_task = (
                    "assemble"
                    +
                    variant
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

                if flavor:

                    artifact_suffix = (
                        "app/build/outputs/apk/"
                        +
                        flavor
                        +
                        "/debug/app-"
                        +
                        flavor
                        +
                        "-debug.apk"
                    )

                else:

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
                        (
                            "app/build/outputs/apk/"
                            +
                            flavor
                            +
                            "/release/app-"
                            +
                            flavor
                            +
                            "-release.apk"
                        )
                        if flavor
                        else (
                            "app/build/outputs/apk/"
                            "release/app-release.apk"
                        )
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
