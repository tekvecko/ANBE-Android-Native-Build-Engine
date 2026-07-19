#!/usr/bin/env python3


from .engine import RecipeEngine
from .rules import RecipeRules



class RecipeBuilder:



    def create(self,ctx):


        RecipeEngine().generate(
            ctx
        )


        RecipeRules().apply(
            ctx
        )


        return ctx

