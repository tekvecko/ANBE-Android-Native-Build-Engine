#!/usr/bin/env python3



class RecipeRules:



    def apply(self,ctx):


        recipe=ctx.recipe



        if (
            ctx.runtime
        ):


            recipe["runtime"]=ctx.runtime



        if (
            ctx.aapt2
        ):


            recipe["aapt2"]=ctx.aapt2



        recipe["environment"]=(
            "termux"
        )



        return ctx

