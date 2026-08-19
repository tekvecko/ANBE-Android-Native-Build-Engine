#!/usr/bin/env python3


from .gradle_doctor import GradleDoctor
from .android_cleaner import AndroidCleaner
from .resource_repair import ResourceRepair
from .frontend_compatibility import FrontendCompatibility
from .native_dependency_compatibility import NativeDependencyCompatibility



class RepairEngine:


    def run(self,ctx):


        ctx.log(
            "[>] Running repair pipeline"
        )


        native_dependency_compatibility = (
            NativeDependencyCompatibility()
            .repair(
                ctx.path
            )
        )

        ctx.runtime[
            "native_dependency_compatibility"
        ] = native_dependency_compatibility

        for action in native_dependency_compatibility[
            "actions"
        ]:

            if (
                action[
                    "type"
                ]
                ==
                "disable_sharp_build"
            ):

                ctx.log(
                    "[✓] Disabled unsupported sharp install script "
                    "on Termux Android ARM64"
                )

        frontend_compatibility = (
            FrontendCompatibility()
            .repair(
                ctx.path
            )
        )

        ctx.runtime[
            "frontend_compatibility"
        ] = frontend_compatibility

        for action in frontend_compatibility[
            "actions"
        ]:

            if (
                action[
                    "type"
                ]
                ==
                "package_dependency"
            ):

                ctx.log(
                    "[✓] SvelteKit static adapter dependency applied"
                )

            elif (
                action[
                    "type"
                ]
                ==
                "svelte_adapter"
            ):

                ctx.log(
                    "[✓] SvelteKit static build enabled"
                )

            elif (
                action[
                    "type"
                ]
                ==
                "capacitor_web_dir"
            ):

                ctx.log(
                    "[✓] Capacitor webDir repaired: "
                    +
                    str(
                        action[
                            "from"
                        ]
                    )
                    +
                    " -> "
                    +
                    str(
                        action[
                            "to"
                        ]
                    )
                )

        GradleDoctor().repair(
            ctx
        )


        AndroidCleaner().repair(
            ctx
        )


        ResourceRepair().repair(
            ctx
        )


        ctx.log(
            "[✓] Repair pipeline finished"
        )


        return ctx

