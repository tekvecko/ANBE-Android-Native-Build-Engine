#!/usr/bin/env python3

from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.context import BuildContext
from anbe.signing_bridge import SigningBridge


def test_signing_bridge_skips_debug_build():

    with TemporaryDirectory() as tmp:

        ctx = BuildContext(
            Path(tmp)
        )

        ctx.build_mode = "debug"

        result = SigningBridge().apply(
            ctx
        )

        assert result is ctx


def test_signing_bridge_debug_does_not_require_android_layout():

    with TemporaryDirectory() as tmp:

        ctx = BuildContext(
            Path(tmp)
        )

        ctx.build_mode = "debug"

        SigningBridge().apply(
            ctx
        )
