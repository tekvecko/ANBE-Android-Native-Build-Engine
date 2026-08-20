#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.resource_repair import ResourceRepair


class Context:

    def __init__(
        self,
        path,
        android_root=".",
    ):

        self.path = str(
            path
        )

        self.recipe = {
            "android_root":
            android_root,
        }

        self.runtime = {}
        self.messages = []


    def log(
        self,
        message,
    ):

        self.messages.append(
            str(message)
        )


def make_manifest(
    root,
    icon="@mipmap/ic_launcher",
):

    root = Path(
        root
    )

    main = (
        root
        /
        "app"
        /
        "src"
        /
        "main"
    )

    main.mkdir(
        parents=True
    )

    manifest = (
        main
        /
        "AndroidManifest.xml"
    )

    manifest.write_text(
        '<manifest xmlns:android='
        '"http://schemas.android.com/apk/res/android">\n'
        '  <application android:icon="'
        +
        icon
        +
        '" '
        'android:roundIcon="@mipmap/ic_launcher_round">\n'
        '  </application>\n'
        '</manifest>\n'
    )

    return manifest


def test_existing_launcher_icon_untouched():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        manifest = make_manifest(
            root
        )

        mipmap = (
            root
            /
            "app"
            /
            "src"
            /
            "main"
            /
            "res"
            /
            "mipmap-mdpi"
        )

        mipmap.mkdir(
            parents=True
        )

        (
            mipmap
            /
            "ic_launcher.png"
        ).write_bytes(
            b"existing"
        )

        assets = root / "assets"
        assets.mkdir()

        (
            assets
            /
            "icon.png"
        ).write_bytes(
            b"fallback"
        )

        original = manifest.read_text()

        ctx = Context(
            root
        )

        ResourceRepair().repair(
            ctx
        )

        assert (
            manifest.read_text()
            ==
            original
        )

        assert (
            "launcher_icon_fallback"
            not in ctx.runtime
        )


def test_missing_launcher_uses_repository_icon():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        manifest = make_manifest(
            root
        )

        assets = root / "assets"
        assets.mkdir()

        source = (
            assets
            /
            "icon.png"
        )

        source.write_bytes(
            b"ANBE-ICON"
        )

        ctx = Context(
            root
        )

        ResourceRepair().repair(
            ctx
        )

        target = (
            root
            /
            "app"
            /
            "src"
            /
            "main"
            /
            "res"
            /
            "drawable"
            /
            "anbe_launcher_icon.png"
        )

        assert target.exists()

        assert (
            target.read_bytes()
            ==
            b"ANBE-ICON"
        )

        text = manifest.read_text()

        assert (
            '@drawable/anbe_launcher_icon'
            in text
        )

        assert (
            ctx.runtime[
                "launcher_icon_fallback"
            ][
                "target"
            ]
            ==
            str(target)
        )


def test_capacitor_android_layout():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        android = (
            root
            /
            "android"
        )

        manifest = make_manifest(
            android
        )

        assets = root / "assets"
        assets.mkdir()

        (
            assets
            /
            "icon.png"
        ).write_bytes(
            b"CAP-ICON"
        )

        ctx = Context(
            root,
            android_root="android",
        )

        ResourceRepair().repair(
            ctx
        )

        assert (
            '@drawable/anbe_launcher_icon'
            in manifest.read_text()
        )

        assert (
            android
            /
            "app"
            /
            "src"
            /
            "main"
            /
            "res"
            /
            "drawable"
            /
            "anbe_launcher_icon.png"
        ).exists()


def test_no_repository_icon_is_safe():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        manifest = make_manifest(
            root
        )

        original = manifest.read_text()

        ctx = Context(
            root
        )

        ResourceRepair().repair(
            ctx
        )

        assert (
            manifest.read_text()
            ==
            original
        )


def test_fallback_idempotent():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        manifest = make_manifest(
            root
        )

        assets = root / "assets"
        assets.mkdir()

        (
            assets
            /
            "icon.png"
        ).write_bytes(
            b"ICON"
        )

        ctx = Context(
            root
        )

        repair = ResourceRepair()

        repair.repair(
            ctx
        )

        first = manifest.read_text()

        repair.repair(
            ctx
        )

        second = manifest.read_text()

        assert first == second

        assert (
            second.count(
                "@drawable/anbe_launcher_icon"
            )
            ==
            2
        )
