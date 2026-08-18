#!/data/data/com.termux/files/usr/bin/python3


class MethodStage:

    def __init__(
        self,
        obj,
        method,
        name=None
    ):

        self.obj = obj
        self.method = method

        self.name = (
            name
            or
            obj.__class__.__name__
        )


    def run(self, ctx):

        result = getattr(
            self.obj,
            self.method
        )(ctx)

        return (
            result
            if result is not None
            else ctx
        )
