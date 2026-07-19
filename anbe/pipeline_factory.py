#!/usr/bin/env python3


from .pipeline import Pipeline
from .stage_adapter import MethodStage

from .detector import ProjectDetector
from .project import ProjectAnalyzer
from .plugin_loader import PluginLoader

from .profile import ProfileEngine, ProfileOptimizer


from .recipe import RecipeBuilder, RecipeExporter

from .artifact import ArtifactEngine
from .export_report import ExportReport
from .manifest import Manifest


class PluginSelectStage:


    def __init__(self):

        self.loader = PluginLoader()
        self.loader.load()


    def run(self, ctx):

        self.loader.select(ctx)



class PipelineFactory:


    def create(self):

        pipeline = Pipeline()


        pipeline.add(
            MethodStage(
                ProjectDetector(),
                "detect"
            )
        )


        pipeline.add(
            MethodStage(
                ProjectAnalyzer(),
                "analyze"
            )
        )


        pipeline.add(
            PluginSelectStage()
        )


        pipeline.add(
            MethodStage(
                ProfileEngine(),
                "detect"
            )
        )


        pipeline.add(
            MethodStage(
                ProfileOptimizer(),
                "optimize"
            )
        )


        pipeline.add(
            MethodStage(
                RecipeBuilder(),
                "create"
            )
        )


        pipeline.add(
            MethodStage(
                RecipeExporter(),
                "save"
            )
        )


        pipeline.add(
            MethodStage(
                ArtifactEngine(),
                "detect"
            )
        )


        pipeline.add(
            MethodStage(
                ArtifactEngine(),
                "export"
            )
        )


        pipeline.add(
            MethodStage(
                ExportReport(),
                "save"
            )
        )


        pipeline.add(
            MethodStage(
                Manifest(),
                "create"
            )
        )


        return pipeline
