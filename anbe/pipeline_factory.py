#!/data/data/com.termux/files/usr/bin/python3

from .pipeline import Pipeline
from .stage_adapter import MethodStage

from .cache import BuildCache

from .detector import ProjectDetector
from .project import ProjectAnalyzer

from .plugin_loader import PluginLoader

from .profile import (
    ProfileEngine,
    ProfileOptimizer,
)

from .build_plan import BuildPlan
from .runtime_detector import RuntimeDetector

from .recipe import (
    RecipeBuilder,
    RecipeExporter,
)

from .adapter import RecipeAdapter
from .repair import RepairEngine
from .aapt2 import AAPT2Manager

from .executor import Executor

from .artifact import ArtifactEngine
from .build_verifier import BuildVerifier

from .export_report import ExportReport
from .manifest import Manifest


class PluginSelectStage:

    name = "Plugin"

    def __init__(self):

        self.loader = PluginLoader()

        self.loader.load()


    def run(self, ctx):

        self.loader.select(ctx)

        return ctx


class PipelineFactory:

    def create(self):

        pipeline = Pipeline()

        artifact = ArtifactEngine()

        pipeline.add(
            MethodStage(
                BuildCache(),
                "load",
                "Cache"
            )
        )

        pipeline.add(
            MethodStage(
                ProjectDetector(),
                "detect",
                "Detector"
            )
        )

        pipeline.add(
            MethodStage(
                ProjectAnalyzer(),
                "analyze",
                "Analyzer"
            )
        )

        pipeline.add(
            PluginSelectStage()
        )

        pipeline.add(
            MethodStage(
                ProfileEngine(),
                "detect",
                "Profile"
            )
        )

        pipeline.add(
            MethodStage(
                ProfileOptimizer(),
                "optimize",
                "ProfileOptimizer"
            )
        )

        pipeline.add(
            MethodStage(
                BuildPlan(),
                "create",
                "BuildPlan"
            )
        )

        pipeline.add(
            MethodStage(
                RuntimeDetector(),
                "detect",
                "Runtime"
            )
        )

        pipeline.add(
            MethodStage(
                RecipeBuilder(),
                "create",
                "Recipe"
            )
        )

        pipeline.add(
            MethodStage(
                RecipeExporter(),
                "save",
                "RecipeExport"
            )
        )

        pipeline.add(
            MethodStage(
                RecipeAdapter(),
                "adapt",
                "Adapter"
            )
        )

        pipeline.add(
            MethodStage(
                RepairEngine(),
                "run",
                "Repair"
            )
        )

        pipeline.add(
            MethodStage(
                AAPT2Manager(),
                "apply",
                "AAPT2"
            )
        )

        pipeline.add(
            MethodStage(
                Executor(),
                "execute",
                "Executor"
            )
        )

        pipeline.add(
            MethodStage(
                artifact,
                "detect",
                "Artifacts"
            )
        )

        pipeline.add(
            MethodStage(
                BuildVerifier(),
                "verify",
                "Verify"
            )
        )

        pipeline.add(
            MethodStage(
                artifact,
                "export",
                "Export"
            )
        )

        pipeline.add(
            MethodStage(
                ExportReport(),
                "save",
                "Report"
            )
        )

        pipeline.add(
            MethodStage(
                Manifest(),
                "create",
                "Manifest"
            )
        )

        return pipeline
