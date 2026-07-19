#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path
import importlib
import traceback


class PluginLoader:

    def __init__(self):

        self.plugins = []

    def load(self):

        self.plugins = []

        root = Path(__file__).parent / "plugins"

        for folder in sorted(root.iterdir()):

            if not folder.is_dir():
                continue

            module = (
                "anbe.plugins."
                + folder.name
                + ".plugin"
            )

            try:

                plugin = (
                    importlib
                    .import_module(module)
                    .Plugin()
                )

                self.plugins.append(plugin)

            except Exception:

                traceback.print_exc()

        return self.plugins

    def select(self, ctx):

        self.load()

        for plugin in self.plugins:

            try:

                if plugin.detect(ctx):

                    plugin.prepare(ctx)

                    ctx.plugin = plugin

                    ctx.log(
                        f"Plugin selected: {plugin.name}"
                    )

                    return plugin

            except Exception:

                traceback.print_exc()

        raise RuntimeError(
            "No compatible plugin found."
        )

