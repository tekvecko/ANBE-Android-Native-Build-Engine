#!/usr/bin/env python3

import re
import shutil
from pathlib import Path


class ResourceRepair:

    ICON_NAME = "anbe_launcher_icon"


    def android_root(
        self,
        ctx,
    ):

        root = Path(
            ctx.path
        )

        configured = (
            getattr(
                ctx,
                "recipe",
                {},
            )
            .get(
                "android_root"
            )
        )

        if configured:

            configured = Path(
                configured
            )

            if configured.is_absolute():

                return configured

            return (
                root
                /
                configured
            )

        for candidate in (
            root / "android",
            root,
        ):

            if (
                candidate
                /
                "app"
                /
                "src"
                /
                "main"
            ).exists():

                return candidate

        return None


    def manifest_file(
        self,
        android_root,
    ):

        if android_root is None:

            return None

        path = (
            Path(android_root)
            /
            "app"
            /
            "src"
            /
            "main"
            /
            "AndroidManifest.xml"
        )

        if path.exists():

            return path

        return None


    def icon_reference(
        self,
        manifest,
    ):

        if not manifest:

            return None

        text = manifest.read_text(
            errors="ignore"
        )

        match = re.search(
            r'android:icon\s*=\s*["\']([^"\']+)["\']',
            text,
        )

        if not match:

            return None

        return match.group(1)


    def resource_exists(
        self,
        android_root,
        reference,
    ):

        if (
            android_root is None
            or
            not reference
        ):

            return False

        match = re.match(
            r"@([A-Za-z0-9_]+)/([A-Za-z0-9_.-]+)$",
            str(reference),
        )

        if not match:

            return False

        kind = match.group(1)
        name = match.group(2)

        res = (
            Path(android_root)
            /
            "app"
            /
            "src"
            /
            "main"
            /
            "res"
        )

        if not res.exists():

            return False

        extensions = (
            ".png",
            ".webp",
            ".xml",
            ".jpg",
            ".jpeg",
        )

        for folder in res.glob(
            kind + "*"
        ):

            if not folder.is_dir():

                continue

            for extension in extensions:

                if (
                    folder
                    /
                    (
                        name
                        +
                        extension
                    )
                ).exists():

                    return True

        return False


    def source_icon(
        self,
        project,
    ):

        project = Path(
            project
        )

        candidates = (
            project / "assets" / "icon.png",
            project / "assets" / "app-icon.png",
            project / "src" / "assets" / "icon.png",
            project / "resources" / "icon.png",
            project / "public" / "icon.png",
            project / "static" / "icon.png",
            project / "icon.png",
        )

        for path in candidates:

            if (
                path.exists()
                and
                path.is_file()
            ):

                return path

        return None


    def install_fallback(
        self,
        android_root,
        source,
    ):

        target = (
            Path(android_root)
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
            (
                self.ICON_NAME
                +
                ".png"
            )
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not target.exists():

            shutil.copy2(
                source,
                target,
            )

        return target


    def update_manifest(
        self,
        manifest,
    ):

        text = manifest.read_text(
            errors="ignore"
        )

        reference = (
            "@drawable/"
            +
            self.ICON_NAME
        )

        updated, count = re.subn(
            r'android:icon\s*=\s*["\'][^"\']+["\']',
            (
                'android:icon="'
                +
                reference
                +
                '"'
            ),
            text,
            count=1,
        )

        if count == 0:

            updated, count = re.subn(
                r"<application\b",
                (
                    '<application android:icon="'
                    +
                    reference
                    +
                    '"'
                ),
                text,
                count=1,
            )

        if count == 0:

            return False

        updated = re.sub(
            r'android:roundIcon\s*=\s*["\'][^"\']+["\']',
            (
                'android:roundIcon="'
                +
                reference
                +
                '"'
            ),
            updated,
            count=1,
        )

        if updated == text:

            return False

        manifest.write_text(
            updated
        )

        return True


    def repair(
        self,
        ctx,
    ):

        project = Path(
            ctx.path
        )

        android_root = (
            self.android_root(
                ctx
            )
        )

        manifest = (
            self.manifest_file(
                android_root
            )
        )

        if not manifest:

            return ctx

        current = (
            self.icon_reference(
                manifest
            )
        )

        if self.resource_exists(
            android_root,
            current,
        ):

            return ctx

        source = self.source_icon(
            project
        )

        if not source:

            return ctx

        target = self.install_fallback(
            android_root,
            source,
        )

        changed = self.update_manifest(
            manifest
        )

        if changed:

            ctx.runtime[
                "launcher_icon_fallback"
            ] = {
                "source":
                str(source),

                "target":
                str(target),

                "reference":
                (
                    "@drawable/"
                    +
                    self.ICON_NAME
                ),
            }

            ctx.log(
                "[✓] Android launcher icon fallback applied"
            )

        return ctx
