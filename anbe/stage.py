#!/usr/bin/env python3


class Stage:


    name = "stage"


    def run(self, ctx):

        raise NotImplementedError(
            "Stage must implement run(ctx)"
        )
