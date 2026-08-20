from pathlib import Path

from anbe.context import BuildContext
from anbe.aapt2 import AAPT2Manager
from anbe.executor import Executor
from anbe.recipe import RecipeBuilder


PROJECT = Path.home() / "rbank"


def test_aapt2_runtime():

    ctx = BuildContext(PROJECT)

    RecipeBuilder().create(ctx)

    AAPT2Manager().apply(ctx)

    assert ctx.aapt2 is not None

    aapt2 = Path(ctx.aapt2)

    assert aapt2.exists()
    assert aapt2.is_file()

    assert ctx.runtime["aapt2"] == str(aapt2)


def test_gradle_command_wiring():

    ctx = BuildContext(PROJECT)

    RecipeBuilder().create(ctx)

    AAPT2Manager().apply(ctx)

    command = Executor().gradle_command(ctx)

    assert "./gradlew" in command

    assert (
        "-Pandroid.aapt2FromMavenOverride="
        + ctx.aapt2
    ) in command

    assert "java-17-openjdk" in command

    assert "clean assembleDebug" in command


if __name__ == "__main__":

    test_aapt2_runtime()
    print("AAPT2 regression OK")

    test_gradle_command_wiring()
    print("Gradle command wiring OK")

    print("ANBE toolchain regression suite OK")
