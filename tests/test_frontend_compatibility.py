from pathlib import Path
from tempfile import TemporaryDirectory
import json

from anbe.frontend_compatibility import FrontendCompatibility


def make_project(
    root,
):

    root = Path(
        root
    )

    (
        root
        /
        "package.json"
    ).write_text(
        json.dumps({
            "scripts": {
                "build":
                "vite build"
            },
            "devDependencies": {
                "@sveltejs/adapter-auto":
                "^3.0.0",
                "@sveltejs/kit":
                "^2.0.0",
                "vite":
                "^5.0.3"
            },
            "dependencies": {
                "@capacitor/core":
                "^5.7.4"
            }
        })
        +
        "\n"
    )

    (
        root
        /
        "svelte.config.js"
    ).write_text(
        "import adapter from "
        "'@sveltejs/adapter-auto';\n"
        "\n"
        "const config = {\n"
        "  kit: {\n"
        "    adapter: adapter()\n"
        "  }\n"
        "};\n"
        "\n"
        "export default config;\n"
    )

    (
        root
        /
        "capacitor.config.ts"
    ).write_text(
        "const config = {\n"
        "  appId: 'example.app',\n"
        "  webDir: 'dist'\n"
        "};\n"
        "\n"
        "export default config;\n"
    )

    return root


def test_svelte_capacitor_repair():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        result = (
            FrontendCompatibility()
            .repair(
                root
            )
        )

        assert result[
            "changed"
        ]

        package = json.loads(
            (
                root
                /
                "package.json"
            ).read_text()
        )

        dev = package[
            "devDependencies"
        ]

        assert (
            "@sveltejs/adapter-auto"
            not in dev
        )

        assert (
            dev[
                "@sveltejs/adapter-static"
            ]
            ==
            "^3.0.0"
        )

        svelte = (
            root
            /
            "svelte.config.js"
        ).read_text()

        assert (
            "@sveltejs/adapter-static"
            in svelte
        )

        assert (
            "fallback: 'index.html'"
            in svelte
        )

        capacitor = (
            root
            /
            "capacitor.config.ts"
        ).read_text()

        assert (
            "webDir: 'build'"
            in capacitor
        )


def test_repair_idempotent():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        compat = (
            FrontendCompatibility()
        )

        first = compat.repair(
            root
        )

        second = compat.repair(
            root
        )

        assert first[
            "changed"
        ]

        assert (
            second[
                "changed"
            ]
            is False
        )


def test_non_svelte_project_unchanged():

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
                "scripts": {
                    "build":
                    "vite build"
                },
                "dependencies": {
                    "react":
                    "^18.0.0"
                }
            })
        )

        (
            root
            /
            "capacitor.config.ts"
        ).write_text(
            "const config = { "
            "webDir: 'dist' "
            "};"
        )

        result = (
            FrontendCompatibility()
            .repair(
                root
            )
        )

        assert (
            result[
                "changed"
            ]
            is False
        )


def test_json_capacitor_config():

    with TemporaryDirectory() as tmp:

        root = make_project(
            tmp
        )

        (
            root
            /
            "capacitor.config.ts"
        ).unlink()

        (
            root
            /
            "capacitor.config.json"
        ).write_text(
            json.dumps({
                "appId":
                "example.app",
                "webDir":
                "dist"
            })
        )

        result = (
            FrontendCompatibility()
            .repair(
                root
            )
        )

        assert result[
            "changed"
        ]

        config = json.loads(
            (
                root
                /
                "capacitor.config.json"
            ).read_text()
        )

        assert (
            config[
                "webDir"
            ]
            ==
            "build"
        )
