from pathlib import Path
from tempfile import TemporaryDirectory
import json

from anbe.context import BuildContext
from anbe.recipe import RecipeBuilder


def commands(ctx):

    return {
        step["id"]:
        step.get("command")
        for step in ctx.recipe["steps"]
        if step.get("type") == "command"
    }


def make_project(
    root,
    package,
    lockfile=None,
):

    root = Path(root)

    (
        root
        /
        "package.json"
    ).write_text(
        json.dumps(package)
    )

    (
        root
        /
        "capacitor.config.json"
    ).write_text("{}")

    if lockfile:

        (
            root
            /
            lockfile
        ).write_text("")

    android = (
        root
        /
        "android"
    )

    android.mkdir()

    (
        android
        /
        "gradlew"
    ).write_text(
        "#!/bin/sh\n"
    )

    ctx = BuildContext(
        root
    )

    RecipeBuilder().create(
        ctx
    )

    return ctx


def test_npm_default():

    with TemporaryDirectory() as tmp:

        ctx = make_project(
            tmp,
            {
                "scripts": {
                    "build":
                    "vite build"
                }
            },
        )

        cmd = commands(ctx)

        assert (
            ctx.recipe[
                "package_manager"
            ]
            ==
            "npm"
        )

        assert (
            cmd[
                "npm-install"
            ]
            ==
            "npm install"
        )

        assert (
            cmd[
                "npm-build"
            ]
            ==
            "npm run build"
        )

        assert (
            cmd[
                "capacitor-sync-android"
            ]
            ==
            "npx cap sync android"
        )


def test_pnpm_package_manager():

    with TemporaryDirectory() as tmp:

        ctx = make_project(
            tmp,
            {
                "packageManager":
                "pnpm@10.28.0",
                "scripts": {
                    "build":
                    "vite build"
                }
            },
        )

        cmd = commands(ctx)

        assert (
            ctx.recipe[
                "package_manager"
            ]
            ==
            "pnpm"
        )

        assert (
            cmd[
                "npm-install"
            ]
            ==
            "pnpm install"
        )

        assert (
            cmd[
                "npm-build"
            ]
            ==
            "pnpm run build"
        )

        assert (
            cmd[
                "capacitor-sync-android"
            ]
            ==
            "pnpm exec cap sync android"
        )


def test_pnpm_lockfile_detection():

    with TemporaryDirectory() as tmp:

        ctx = make_project(
            tmp,
            {
                "scripts": {
                    "build":
                    "vite build"
                }
            },
            lockfile="pnpm-lock.yaml",
        )

        assert (
            ctx.recipe[
                "package_manager"
            ]
            ==
            "pnpm"
        )


def test_yarn_lockfile_detection():

    with TemporaryDirectory() as tmp:

        ctx = make_project(
            tmp,
            {
                "scripts": {
                    "build":
                    "vite build"
                }
            },
            lockfile="yarn.lock",
        )

        cmd = commands(ctx)

        assert (
            ctx.recipe[
                "package_manager"
            ]
            ==
            "yarn"
        )

        assert (
            cmd[
                "npm-install"
            ]
            ==
            "yarn install"
        )

        assert (
            cmd[
                "npm-build"
            ]
            ==
            "yarn build"
        )
