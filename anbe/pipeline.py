#!/usr/bin/env python3


class Pipeline:

    def __init__(self):
        self.stages = []


    def add(self, stage):

        self.stages.append(stage)

        return self


    def run(self, ctx):

        for stage in self.stages:

            ctx.log(
                "[stage] " + stage.__class__.__name__
            )

            stage.run(ctx)

        return ctx
