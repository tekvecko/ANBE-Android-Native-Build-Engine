#!/usr/bin/env python3

from pathlib import Path


class SigningBridge:

    START = "// ANBE RELEASE SIGNING START"
    END = "// ANBE RELEASE SIGNING END"

    BLOCK = r'''
// ANBE RELEASE SIGNING START
def anbeReleaseStoreFile = project.findProperty("ANBE_RELEASE_STORE_FILE")
def anbeReleaseStorePassword = project.findProperty("ANBE_RELEASE_STORE_PASSWORD")
def anbeReleaseKeyAlias = project.findProperty("ANBE_RELEASE_KEY_ALIAS")
def anbeReleaseKeyPassword = project.findProperty("ANBE_RELEASE_KEY_PASSWORD")

def anbeReleaseSigningConfigured =
        anbeReleaseStoreFile &&
        anbeReleaseStorePassword &&
        anbeReleaseKeyAlias &&
        anbeReleaseKeyPassword
// ANBE RELEASE SIGNING END
'''.strip()

    SIGNING_CONFIG = r'''
        if (anbeReleaseSigningConfigured) {
            signingConfigs {
                anbeRelease {
                    storeFile file(anbeReleaseStoreFile)
                    storePassword anbeReleaseStorePassword
                    keyAlias anbeReleaseKeyAlias
                    keyPassword anbeReleaseKeyPassword
                }
            }
        }
'''.strip()

    RELEASE_LINK = r'''
            if (anbeReleaseSigningConfigured) {
                signingConfig signingConfigs.anbeRelease
            }
'''.strip()


    def apply(self, ctx):

        if (
            getattr(
                ctx,
                "build_mode",
                "debug",
            )
            !=
            "release"
        ):

            ctx.log(
                "ANBE signing bridge skipped for debug build"
            )

            return ctx

        android_root = Path(
            ctx.path
        ) / "android"

        app_gradle = (
            android_root
            /
            "app"
            /
            "build.gradle"
        )

        if not app_gradle.exists():

            raise RuntimeError(
                "Groovy app/build.gradle not found: "
                +
                str(app_gradle)
            )

        text = app_gradle.read_text()

        changed = False

        if self.START not in text:

            marker = (
                "apply plugin: "
                "'com.android.application'"
            )

            if marker not in text:

                raise RuntimeError(
                    "Android application plugin marker not found"
                )

            text = text.replace(
                marker,
                marker
                +
                "\n\n"
                +
                self.BLOCK,
                1
            )

            changed = True

        if (
            "signingConfigs {\n"
            "                anbeRelease"
            not in text
        ):

            marker = "android {"

            if marker not in text:

                raise RuntimeError(
                    "android block not found"
                )

            text = text.replace(
                marker,
                marker
                +
                "\n"
                +
                self.SIGNING_CONFIG
                +
                "\n",
                1
            )

            changed = True

        if (
            "signingConfig signingConfigs.anbeRelease"
            not in text
        ):

            marker = '''        release {
'''

            if marker not in text:

                raise RuntimeError(
                    "release buildType block not found"
                )

            text = text.replace(
                marker,
                marker
                +
                self.RELEASE_LINK
                +
                "\n",
                1
            )

            changed = True

        if changed:

            app_gradle.write_text(
                text
            )

            ctx.log(
                "ANBE signing bridge applied"
            )

        else:

            ctx.log(
                "ANBE signing bridge already present"
            )

        return ctx
