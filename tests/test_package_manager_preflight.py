from pathlib import Path
from tempfile import TemporaryDirectory
import json

from anbe.package_manager import PackageManagerResolver
from anbe.preflight import Preflight


class FakeToolchain:

    def resolve(self):

        return {
            "aapt2":
            "/fake/aapt2",

            "aidl":
            None,

            "zipalign":
            None,

            "apksigner":
            None,
        }


class FakeJavaResolver:

    def gradle_version(
        self,
        root
    ):

        return "8.14"


    def required_java(
        self,
        root
    ):

        return 21


    def resolve(
        self,
        root
    ):

        return "/fake/java-21"


def make_project(
    root,
    package,
):

    root = Path(
        root
    )

    (
        root
        /
        "package.json"
    ).write_text(
        json.dumps(
            package
        )
    )

    (
        root
        /
        "capacitor.config.ts"
    ).write_text(
        "export default {}"
    )

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

    return root


def fake_which(
    available
):

    def which(name):

        if name in available:

            return (
                "/fake/bin/"
                +
                name
            )

        return None

    return which


def check_map(
    report
):

    return {
        item[
            "name"
        ]:
        item
        for item in report[
            "checks"
        ]
    }


def test_resolver_declared_pnpm():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        (
            root
            /
            "package.json"
        ).write_text(
            json.dumps({
                "packageManager":
                "pnpm@10.28.0+sha512.test"
            })
        )

        info = (
            PackageManagerResolver()
            .detect(
                root
            )
        )

        assert (
            info[
                "name"
            ]
            ==
            "pnpm"
        )

        assert (
            info[
                "version"
            ]
            ==
            "10.28.0"
        )


def test_preflight_pnpm_missing():

    with TemporaryDirectory() as tmp:

        root = make_project(
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

        preflight = Preflight(
            java_resolver=(
                FakeJavaResolver()
            ),
            android_toolchain=(
                FakeToolchain()
            ),
            which=fake_which({
                "node",
                "corepack",
            }),
        )

        report = preflight.inspect(
            root
        )

        checks = check_map(
            report
        )

        assert (
            checks[
                "package_manager"
            ][
                "status"
            ]
            ==
            "FAIL"
        )

        assert (
            "pnpm@10.28.0"
            in
            checks[
                "package_manager"
            ][
                "value"
            ]
        )

        assert (
            "corepack"
            in
            checks[
                "package_manager"
            ][
                "message"
            ]
        )

        assert (
            report[
                "ready"
            ]
            is False
        )


def test_preflight_pnpm_available():

    with TemporaryDirectory() as tmp:

        root = make_project(
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

        preflight = Preflight(
            java_resolver=(
                FakeJavaResolver()
            ),
            android_toolchain=(
                FakeToolchain()
            ),
            which=fake_which({
                "node",
                "pnpm",
            }),
        )

        report = preflight.inspect(
            root
        )

        checks = check_map(
            report
        )

        assert (
            checks[
                "package_manager"
            ][
                "status"
            ]
            ==
            "PASS"
        )

        assert (
            checks[
                "capacitor_runner"
            ][
                "status"
            ]
            ==
            "PASS"
        )


def test_preflight_npm_compatibility():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp,
            {
                "scripts": {
                    "build":
                    "vite build"
                }
            },
        )

        preflight = Preflight(
            java_resolver=(
                FakeJavaResolver()
            ),
            android_toolchain=(
                FakeToolchain()
            ),
            which=fake_which({
                "node",
                "npm",
                "npx",
            }),
        )

        report = preflight.inspect(
            root
        )

        checks = check_map(
            report
        )

        assert (
            checks[
                "package_manager"
            ][
                "status"
            ]
            ==
            "PASS"
        )

        assert (
            checks[
                "package_manager"
            ][
                "value"
            ].startswith(
                "npm"
            )
        )

        assert (
            checks[
                "capacitor_runner"
            ][
                "status"
            ]
            ==
            "PASS"
        )
