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

