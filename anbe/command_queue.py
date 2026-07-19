#!/data/data/com.termux/files/usr/bin/python3

from .process import ProcessRunner


class CommandQueue:

    def __init__(self):

        self.runner = ProcessRunner()

        self.results = []

    def add(
        self,
        command,
        cwd=None
    ):

        self.results.append(
            self.runner.run(
                command,
                cwd=cwd
            )
        )

    def execute(self):

        return self.results

