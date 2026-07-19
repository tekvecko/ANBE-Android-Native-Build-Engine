#!/usr/bin/env python3


from .gradle_doctor import GradleDoctor
from .android_cleaner import AndroidCleaner
from .resource_repair import ResourceRepair



class RepairEngine:


    def run(self,ctx):


        ctx.log(
            "[>] Running repair pipeline"
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

