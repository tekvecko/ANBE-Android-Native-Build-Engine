#!/data/data/com.termux/files/usr/bin/python3

from .command_queue import CommandQueue


class Executor:

    def execute(self, ctx):

        q = CommandQueue()

        root = str(ctx.path)

        q.add(
            "npm install",
            cwd=root
        )

        q.add(
            "npm run build",
            cwd=root
        )

        q.add(
            "npx cap sync android",
            cwd=root
        )

        q.add(
            "cd android && ./gradlew clean assembleDebug --stacktrace",
            cwd=root
        )

        ctx.execution = q.execute()

        ctx.log(
            "Build executed"
        )

