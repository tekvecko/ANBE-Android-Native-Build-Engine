#!/usr/bin/env python3


from .gradle_doctor import GradleDoctor
from .android_cleaner import AndroidCleaner
from .resource_repair import ResourceRepair
from .frontend_compatibility import FrontendCompatibility



class RepairEngine:


    def run(self,ctx):


        ctx.log(
            "[>] Running repair pipeline"
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

