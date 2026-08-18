from pathlib import Path

from anbe.context import BuildContext
from anbe.java_resolver import JavaResolver
from anbe.recipe import RecipeBuilder
from anbe.pipeline_factory import PipelineFactory


PROJECT = Path.home() / "rbank"


def test_java_resolver():

    root = PROJECT / "android"

    resolver = JavaResolver()

    assert resolver.gradle_version(root) == "8.2"
    assert resolver.project_java_version(root) == 21
    assert resolver.required_java(root) == 21

    resolved = resolver.resolve(root)

    assert resolved is not None
    assert resolved.endswith(
        "java-21-openjdk"
    )


def test_recipe_android_discovery():

    ctx = BuildContext(
        PROJECT
    )

    RecipeBuilder().create(ctx)

    assert ctx.recipe["android_root"] == "android"

    gradle_steps = [
        step
        for step in ctx.recipe["steps"]
        if (
            isinstance(step, dict)
            and
            step.get("type") == "gradle"
        )
    ]

    assert len(gradle_steps) == 1
    assert gradle_steps[0]["task"] == "assembleDebug"

    assert ctx.recipe["artifact"] == {
        "type": "apk",
        "path":
        "android/app/build/outputs/apk/debug/app-debug.apk"
    }


def test_pipeline_stage_contract():

    pipeline = PipelineFactory().create()

    names = [
        pipeline.stage_name(stage)
        for stage in pipeline.stages
    ]

    assert names == [
        "Cache",
        "Detector",
        "Analyzer",
        "Plugin",
        "Profile",
        "ProfileOptimizer",
        "BuildPlan",
        "Runtime",
        "Recipe",
        "RecipeExport",
        "Adapter",
        "Repair",
        "AAPT2",
        "Executor",
        "Artifacts",
        "Verify",
        "Export",
        "Report",
        "Manifest",
    ]


if __name__ == "__main__":

    test_java_resolver()

    print(
        "JavaResolver regression OK"
    )

    test_recipe_android_discovery()

    print(
        "Recipe regression OK"
    )

    test_pipeline_stage_contract()

    print(
        "Pipeline contract regression OK"
    )

    print(
        "ANBE framework regression suite OK"
    )
