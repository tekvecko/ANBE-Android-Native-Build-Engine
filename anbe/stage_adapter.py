#!/usr/bin/env python3


class MethodStage:


    def __init__(self, obj, method):

        self.obj = obj
        self.method = method


    def run(self, ctx):

        getattr(
            self.obj,
            self.method
        )(ctx)
