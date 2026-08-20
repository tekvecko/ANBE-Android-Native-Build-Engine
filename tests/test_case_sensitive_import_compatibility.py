#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.case_sensitive_import_compatibility import (
    CaseSensitiveImportCompatibility,
)


def test_case_sensitive_import_repaired():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        src = (
            root
            /
            "src"
        )

        src.mkdir()

        (
            src
            /
            "base64images.ts"
        ).write_text(
            "export const Images = [];\n"
        )

        target = (
            src
            /
            "index.ts"
        )

        target.write_text(
            "import { Images } from './base64Images';\n"
        )

        result = (
            CaseSensitiveImportCompatibility()
            .repair(
                root
            )
        )

        assert result[
            "changed"
        ]

        text = target.read_text()

        assert (
            "./base64images"
            in text
        )

        assert (
            "./base64Images"
            not in text
        )


def test_case_sensitive_import_idempotent():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        src = (
            root
            /
            "src"
        )

        src.mkdir()

        (
            src
            /
            "base64images.ts"
        ).write_text(
            "export const Images = [];\n"
        )

        target = (
            src
            /
            "index.ts"
        )

        target.write_text(
            "import { Images } from './base64Images';\n"
        )

        compat = (
            CaseSensitiveImportCompatibility()
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


def test_existing_exact_import_unchanged():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        src = (
            root
            /
            "src"
        )

        src.mkdir()

        (
            src
            /
            "utils.ts"
        ).write_text(
            "export const x = 1;\n"
        )

        target = (
            src
            /
            "index.ts"
        )

        target.write_text(
            "import { x } from './utils';\n"
        )

        result = (
            CaseSensitiveImportCompatibility()
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


def test_ambiguous_case_match_unchanged():

    with TemporaryDirectory() as tmp:

        root = Path(
            tmp
        )

        src = (
            root
            /
            "src"
        )

        src.mkdir()

        (
            src
            /
            "foo.ts"
        ).write_text(
            "export const a = 1;\n"
        )

        (
            src
            /
            "FOO.ts"
        ).write_text(
            "export const b = 2;\n"
        )

        target = (
            src
            /
            "index.ts"
        )

        target.write_text(
            "import './Foo';\n"
        )

        result = (
            CaseSensitiveImportCompatibility()
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
