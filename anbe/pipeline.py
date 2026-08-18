#!/data/data/com.termux/files/usr/bin/python3

from .core.validator import ContextValidator


class Pipeline:

    def __init__(self):

        self.stages = []

        self.validator = ContextValidator()


    def add(self, stage):

        self.stages.append(stage)

        return self


    def stage_name(self, stage):

        return getattr(
            stage,
            "name",
            stage.__class__.__name__
        )


    def run(self, ctx):

        self.validator.check(
            ctx,
            "Context"
        )

        for stage in self.stages:

            name = self.stage_name(
                stage
            )

            print()
            print(
                "----------------------------------------"
            )
            print(
                "[STAGE]",
                name
            )
            print(
                "----------------------------------------"
            )

            stage.run(ctx)

            self.validator.check(
                ctx,
                name
            )

        return ctx
