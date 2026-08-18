#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path

from .logger import Logger


class BuildContext:

    def __init__(self, path):

        self.logger = Logger()

        self.path = Path(path)

        self.project = {}

        self.profile = {}

        self.recipe = {}

        self.plan = {}

        self.runtime = {}

        self.aapt2 = None
    
        self.gradle = None

        self.npm = None

        self.workspace = {}

        self.cache = {}

        self.plugin = None

        self.artifacts = []

        self.exports = []

        self.execution = []

        self.meta = {}

        self.build_mode = "debug"

        self.artifact_format = "apk"

    def set(self, name, value):

        setattr(self, name, value)

        return value

    def get(self, name, default=None):

        return getattr(
            self,
            name,
            default
        )

    def append(self, name, value):

        lst = getattr(
            self,
            name,
            None
        )

        if lst is None:

            lst = []

            setattr(
                self,
                name,
                lst
            )

        lst.append(value)

        return lst

    def log(self, msg):

        self.logger.ok(msg)

    def info(self, msg):

        self.logger.info(msg)

    def warn(self, msg):

        self.logger.warn(msg)

    def error(self, msg):

        self.logger.error(msg)


    def validate(self):

        from .core.context_schema import ContextSchema

        ContextSchema.assert_valid(
            self
        )

        return True


    def snapshot(self):

        return {
            "path": str(self.path),

            "project": self.project,
            "profile": self.profile,
            "recipe": self.recipe,
            "plan": self.plan,

            "runtime": self.runtime,
            "workspace": self.workspace,
            "cache": self.cache,

            "plugin": (
                getattr(
                    self.plugin,
                    "name",
                    None
                )
                if self.plugin
                else None
            ),

            "aapt2": self.aapt2,
            "gradle": self.gradle,
            "npm": self.npm,

            "artifacts": [
                str(x)
                for x in self.artifacts
            ],

            "exports": [
                str(x)
                for x in self.exports
            ],

            "execution": self.execution,
            "meta": self.meta,

            "build_mode": self.build_mode,
            "artifact_format": self.artifact_format,
        }
