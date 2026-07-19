#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path

from .core.context import BuildContext

from .core.validator import ContextValidator

from .cache import BuildCache

from .plugin_loader import PluginLoader

from .detector import ProjectDetector

from .project_analyzer import ProjectAnalyzer

from .runtime_detector import RuntimeDetector

from .profile_engine import ProfileEngine

from .profile_optimizer import ProfileOptimizer

from .build_plan import BuildPlan

from .recipe import RecipeBuilder

from .recipe import RecipeExporter

from .adapter import RecipeAdapter

from .repair import RepairEngine

from .aapt2 import AAPT2Manager

from .executor import Executor

from .artifact import ArtifactEngine

from .export_report import ExportReport

from .manifest import Manifest


class Builder:


    def __init__(self):

        self.validator = ContextValidator()


    def stage(self,name,fn,ctx):

        print()

        print("----------------------------------------")

        print("[STAGE]",name)

        print("----------------------------------------")

        fn(ctx)

        self.validator.check(

            ctx,

            name

        )


    def build(self,path):

        ctx=BuildContext(

            Path(path).expanduser()

        )


        self.validator.check(

            ctx,

            "Context"

        )


        self.stage(

            "Cache",

            lambda c: BuildCache().load(c),

            ctx

        )


        self.stage(

            "Detector",

            lambda c: ProjectDetector().detect(c),

            ctx

        )


        self.stage(

            "Analyzer",

            lambda c: ProjectAnalyzer().analyze(c),

            ctx

        )


        loader=PluginLoader()

        loader.load()

        loader.select(ctx)


        self.validator.check(

            ctx,

            "Plugin"

        )


        self.stage(

            "Profile",

            lambda c: ProfileEngine().detect(c),

            ctx

        )


        self.stage(

            "ProfileOptimizer",

            lambda c: ProfileOptimizer().optimize(c),

            ctx

        )


        self.stage(

            "BuildPlan",

            lambda c: BuildPlan().create(c),

            ctx

        )


        self.stage(

            "Runtime",

            lambda c: RuntimeDetector().detect(c),

            ctx

        )


        self.stage(

            "Recipe",

            lambda c: RecipeBuilder().create(c),

            ctx

        )


        self.stage(

            "RecipeExport",

            lambda c: RecipeExporter().save(c),

            ctx

        )


        self.stage(

            "Adapter",

            lambda c: RecipeAdapter().adapt(c),

            ctx

        )


        self.stage(

            "Repair",

            lambda c: RepairEngine().run(c),

            ctx

        )


        self.stage(

            "AAPT2",

            lambda c: AAPT2Manager().apply(c),

            ctx

        )


        self.stage(

            "Executor",

            lambda c: Executor().execute(c),

            ctx

        )


        self.stage(

            "Artifacts",

            lambda c: ArtifactEngine().detect(c),

            ctx

        )


        self.stage(

            "Export",

            lambda c: ArtifactEngine().export(c),

            ctx

        )


        self.stage(

            "Report",

            lambda c: ExportReport().save(c),

            ctx

        )


        self.stage(

            "Manifest",

            lambda c: Manifest().create(c),

            ctx

        )


        return ctx

